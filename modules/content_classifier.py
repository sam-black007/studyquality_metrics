"""
Module 3: Screen Content Classification

This module uses transfer learning with MobileNetV2 to classify screen content into:
- STUDY (PDFs, code editors, documentation, slides)
- EDUCATIONAL_VIDEO (long-form learning videos)
- DISTRACTION_VIDEO (short-form videos, reels, entertainment)
- SOCIAL_MEDIA (social feeds, messaging)
- OTHER (everything else)

Special logic for YouTube detection to differentiate educational vs distracting content.

Author: AI Study Focus Monitor
"""

import numpy as np
from PIL import Image
import logging
import sys
import os
import cv2

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import ContentCategory, load_config

logger = logging.getLogger(__name__)

# Try to import TensorFlow
try:
    import tensorflow as tf
    from tensorflow import keras
    TF_AVAILABLE = True
except ImportError:
    logger.warning("TensorFlow not available, using rule-based classification only")
    TF_AVAILABLE = False


class ContentClassifier:
    """
    Classifies screen content using ML and heuristics.
    """
    
    def __init__(self, config: dict):
        """
        Initialize the content classifier.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.model_config = config.get('model', {})
        self.input_size = self.model_config.get('input_size', 224)
        self.confidence_threshold = self.model_config.get('confidence_threshold', 0.6)
        
        self.model = None
        self.model_loaded = False
        
        logger.info("ContentClassifier initialized")
    
    def load_model(self):
        """
        Load or create the ML model for classification.
        """
        if not TF_AVAILABLE:
            logger.warning("Skipping model loading (TensorFlow not available)")
            return
        
        model_path = self.model_config.get('classifier_path', 'models/screen_classifier.h5')
        
        # Check if pre-trained model exists
        if os.path.exists(model_path):
            try:
                self.model = keras.models.load_model(model_path)
                self.model_loaded = True
                logger.info(f"Loaded model from {model_path}")
                return
            except Exception as e:
                logger.warning(f"Failed to load model from {model_path}: {e}")
        
        # Create a new model using transfer learning
        logger.info("Creating new model with MobileNetV2...")
        self._create_model()
    
    def _create_model(self):
        """
        Create a new classification model using MobileNetV2 transfer learning.
        """
        if not TF_AVAILABLE:
            return
        
        # Load pre-trained MobileNetV2
        base_model = keras.applications.MobileNetV2(
            input_shape=(self.input_size, self.input_size, 3),
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Create new model
        inputs = keras.Input(shape=(self.input_size, self.input_size, 3))
        x = base_model(inputs, training=False)
        x = keras.layers.GlobalAveragePooling2D()(x)
        x = keras.layers.Dropout(0.2)(x)
        x = keras.layers.Dense(128, activation='relu')(x)
        x = keras.layers.Dropout(0.2)(x)
        outputs = keras.layers.Dense(5, activation='softmax')(x)  # 5 categories
        
        self.model = keras.Model(inputs, outputs)
        
        # Compile model
        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model_loaded = True
        logger.info("Model created successfully")
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess image for model input.
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed numpy array
        """
        # Resize to model input size
        img_resized = image.resize((self.input_size, self.input_size))
        
        # Convert to numpy array
        img_array = np.array(img_resized, dtype=np.float32)
        
        # Normalize to [0, 1]
        img_array = img_array / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def detect_youtube(self, image: Image.Image) -> tuple:
        """
        Detect if YouTube is open and determine video type (educational vs distraction).
        
        Args:
            image: PIL Image of screen
            
        Returns:
            Tuple of (is_youtube, video_type) where video_type is ContentCategory or None
        """
        # Convert to OpenCV format
        img_array = np.array(image)
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Convert to HSV for color detection
        hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
        
        # Detect YouTube's red color (approximation)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)
        
        red_pixels = np.sum(red_mask > 0)
        total_pixels = img_cv.shape[0] * img_cv.shape[1]
        red_ratio = red_pixels / total_pixels
        
        # Check for YouTube branding (rough heuristic)
        is_youtube = red_ratio > 0.001  # Adjust threshold as needed
        
        if not is_youtube:
            return False, None
        
        # Determine video type based on aspect ratio and layout
        height, width = img_cv.shape[:2]
        
        # Look for video player region (typically centered)
        # This is a simplified heuristic - in production, you'd use more sophisticated detection
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Detect large dark rectangles (video players)
        _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        largest_contour = None
        largest_area = 0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > largest_area:
                largest_area = area
                largest_contour = contour
        
        if largest_contour is not None:
            x, y, w, h = cv2.boundingRect(largest_contour)
            aspect_ratio = w / h if h > 0 else 0
            
            # Wide horizontal video (16:9 or similar) = educational
            # Vertical video (9:16) = shorts/distraction
            if aspect_ratio > 1.5:  # Horizontal video
                logger.debug(f"YouTube detected: Horizontal video (AR: {aspect_ratio:.2f})")
                return True, ContentCategory.EDUCATIONAL_VIDEO
            elif aspect_ratio < 0.7:  # Vertical video
                logger.debug(f"YouTube detected: Vertical video/Shorts (AR: {aspect_ratio:.2f})")
                return True, ContentCategory.DISTRACTION_VIDEO
        
        # Default to educational if we can't determine
        logger.debug("YouTube detected: Default to educational")
        return True, ContentCategory.EDUCATIONAL_VIDEO
    
    def detect_code_editor(self, image: Image.Image) -> bool:
        """
        Detect if a code editor is open using heuristics.
        
        Args:
            image: PIL Image of screen
            
        Returns:
            True if likely a code editor
        """
        img_array = np.array(image)
        
        # Check for dark background (common in code editors)
        avg_brightness = np.mean(img_array)
        
        # Check for monospace font patterns (high edge density in text regions)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Code editors typically have dark backgrounds with high edge density
        is_code_editor = avg_brightness < 100 and edge_density > 0.05
        
        if is_code_editor:
            logger.debug(f"Code editor detected (brightness: {avg_brightness:.1f}, edges: {edge_density:.3f})")
        
        return is_code_editor
    
    def detect_pdf_reader(self, image: Image.Image) -> bool:
        """
        Detect if a PDF reader is open.
        
        Args:
            image: PIL Image of screen
            
        Returns:
            True if likely a PDF reader
        """
        img_array = np.array(image)
        
        # PDF readers typically have white/light backgrounds with text
        avg_brightness = np.mean(img_array)
        
        # High brightness suggests document reader
        is_pdf = avg_brightness > 200
        
        if is_pdf:
            logger.debug(f"PDF reader detected (brightness: {avg_brightness:.1f})")
        
        return is_pdf
    
    def classify_screen(self, screen_image: Image.Image) -> ContentCategory:
        """
        Classify the screen content into a category.
        
        Args:
            screen_image: PIL Image of the screen
            
        Returns:
            ContentCategory enum value
        """
        # Rule-based detection first (more accurate for specific cases)
        
        # Check for YouTube
        is_youtube, video_type = self.detect_youtube(screen_image)
        if is_youtube and video_type is not None:
            return video_type
        
        # Check for code editor
        if self.detect_code_editor(screen_image):
            return ContentCategory.STUDY
        
        # Check for PDF reader
        if self.detect_pdf_reader(screen_image):
            return ContentCategory.STUDY
        
        # If ML model is available, use it for classification
        if self.model_loaded and self.model is not None:
            try:
                # Preprocess image
                img_processed = self.preprocess_image(screen_image)
                
                # Predict
                predictions = self.model.predict(img_processed, verbose=0)
                predicted_class = np.argmax(predictions[0])
                confidence = predictions[0][predicted_class]
                
                # Map index to category
                category_map = {
                    0: ContentCategory.STUDY,
                    1: ContentCategory.EDUCATIONAL_VIDEO,
                    2: ContentCategory.DISTRACTION_VIDEO,
                    3: ContentCategory.SOCIAL_MEDIA,
                    4: ContentCategory.OTHER
                }
                
                category = category_map.get(predicted_class, ContentCategory.OTHER)
                
                logger.debug(f"ML Classification: {category.value} (confidence: {confidence:.2f})")
                
                # Return prediction if confidence is high enough
                if confidence >= self.confidence_threshold:
                    return category
                
            except Exception as e:
                logger.error(f"Error in ML classification: {e}")
        
        # Default to OTHER if no clear classification
        logger.debug("Classification: OTHER (default)")
        return ContentCategory.OTHER


def main():
    """
    Test the ContentClassifier module independently.
    """
    import time
    from screen_capture import ScreenCapture
    
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Load config
    config = load_config()
    
    # Initialize modules
    classifier = ContentClassifier(config)
    classifier.load_model()
    
    capture = ScreenCapture(config)
    
    print("Content classifier running...")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        for i in range(5):  # Test 5 times
            screen = capture.capture_screen()
            category = classifier.classify_screen(screen)
            print(f"Classification {i+1}: {category.value}")
            time.sleep(capture.interval)
            
    except KeyboardInterrupt:
        print("\n\nStopping...")
    finally:
        capture.close()


if __name__ == "__main__":
    main()
