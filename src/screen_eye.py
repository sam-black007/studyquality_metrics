"""
Screen Capture and Classification Module
Captures screen and classifies content type
"""
import mss
import numpy as np
from PIL import Image
import tensorflow as tf
from typing import Tuple, Dict, Optional
import os

from src.config import (
    SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT,
    SCREEN_CLASSES, CONFIDENCE_THRESHOLD,
    SCREEN_CLASSIFIER_MODEL
)


class ScreenCapturer:
    """Captures screenshots efficiently using mss"""
    
    def __init__(self):
        self.sct = mss.mss()
        
    def capture(self) -> np.ndarray:
        """
        Capture the primary monitor screen
        
        Returns:
            RGB numpy array of screen
        """
        # Capture primary monitor
        monitor = self.sct.monitors[1]
        screenshot = self.sct.grab(monitor)
        
        # Convert to numpy array
        img = np.array(screenshot)
        
        # Convert BGRA to RGB
        img = img[:, :, :3]
        
        return img
    
    def capture_and_resize(self, target_size: Tuple[int, int] = None) -> np.ndarray:
        """
        Capture and resize for model input
        
        Args:
            target_size: (width, height) tuple, defaults to config values
            
        Returns:
            Resized RGB image
        """
        if target_size is None:
            target_size = (SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT)
            
        img = self.capture()
        
        # Resize using PIL for better quality
        pil_img = Image.fromarray(img)
        pil_img = pil_img.resize(target_size, Image.Resampling.LANCZOS)
        
        return np.array(pil_img)
    
    def close(self):
        """Release resources"""
        self.sct.close()


class ScreenClassifier:
    """
    Classifies screen content using trained CNN model
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize classifier
        
        Args:
            model_path: Path to trained .h5 model file
        """
        self.model_path = model_path or SCREEN_CLASSIFIER_MODEL
        self.model = None
        self.classes = SCREEN_CLASSES
        
        # Try to load model if it exists
        if os.path.exists(self.model_path):
            self.load_model()
        else:
            print(f"Warning: Model not found at {self.model_path}")
            print("Please train the model using train_model.py")
            print("Using heuristic fallback for now")
    
    def load_model(self):
        """Load the trained model"""
        try:
            self.model = tf.keras.models.load_model(self.model_path)
            print(f"Model loaded from {self.model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    def preprocess_image(self, img: np.ndarray) -> np.ndarray:
        """
        Preprocess image for model input
        
        Args:
            img: RGB image array
            
        Returns:
            Preprocessed image ready for model
        """
        # Ensure correct size
        if img.shape[:2] != (SCREENSHOT_HEIGHT, SCREENSHOT_WIDTH):
            pil_img = Image.fromarray(img)
            pil_img = pil_img.resize((SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT))
            img = np.array(pil_img)
        
        # Normalize to [0, 1]
        img = img.astype(np.float32) / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img
    
    def predict(self, img: np.ndarray) -> Dict:
        """
        Classify screen content
        
        Args:
            img: RGB image array (any size, will be resized)
            
        Returns:
            Dictionary with:
                - class: predicted class name
                - confidence: prediction confidence
                - all_probabilities: dict of all class probabilities
        """
        if self.model is None:
            # Fallback to heuristic
            return self._heuristic_classify(img)
        
        # Preprocess
        processed = self.preprocess_image(img)
        
        # Predict
        predictions = self.model.predict(processed, verbose=0)[0]
        
        # Get top prediction
        top_idx = np.argmax(predictions)
        top_class = self.classes[top_idx]
        top_confidence = float(predictions[top_idx])
        
        # Build probability dict
        all_probs = {cls: float(prob) for cls, prob in zip(self.classes, predictions)}
        
        # If confidence is too low, classify as OTHER
        if top_confidence < CONFIDENCE_THRESHOLD:
            top_class = "OTHER"
        
        return {
            "class": top_class,
            "confidence": top_confidence,
            "all_probabilities": all_probs
        }
    
    def _heuristic_classify(self, img: np.ndarray) -> Dict:
        """
        Simple heuristic classification when model is not available
        Uses basic image statistics
        
        Args:
            img: RGB image
            
        Returns:
            Classification result
        """
        # Very basic heuristic: check if image is mostly dark (video)
        # or bright (documents/code)
        
        brightness = np.mean(img)
        
        # Simple rule-based classification
        if brightness > 200:
            predicted_class = "STUDY"  # Bright = likely documents
        elif brightness < 100:
            predicted_class = "DISTRACTION_VIDEO"  # Dark = likely video
        else:
            predicted_class = "OTHER"
        
        return {
            "class": predicted_class,
            "confidence": 0.5,  # Low confidence for heuristic
            "all_probabilities": {cls: 0.2 for cls in self.classes}
        }


class ScreenAnalyzer:
    """
    Combined screen capture and classification
    """
    
    def __init__(self, model_path: str = None):
        self.capturer = ScreenCapturer()
        self.classifier = ScreenClassifier(model_path)
    
    def analyze(self) -> Dict:
        """
        Capture and classify current screen
        
        Returns:
            Classification result with screen class and confidence
        """
        # Capture screen
        screen = self.capturer.capture_and_resize()
        
        # Classify
        result = self.classifier.predict(screen)
        
        return result
    
    def close(self):
        """Release resources"""
        self.capturer.close()
