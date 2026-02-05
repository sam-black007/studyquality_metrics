"""
Module 1: Face & Attention Tracking

This module uses webcam input to track user attention state using:
- MediaPipe Face Mesh for facial landmarks
- Eye gaze direction tracking
- Blink rate detection for drowsiness
- Head pose estimation

Author: AI Study Focus Monitor
"""

import cv2
import mediapipe as mp
import numpy as np
from collections import deque
from datetime import datetime
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import AttentionState, calculate_eye_aspect_ratio, load_config

logger = logging.getLogger(__name__)


class FaceTracker:
    """
    Tracks user attention state using webcam and facial analysis.
    """
    
    def __init__(self, config: dict):
        """
        Initialize the face tracker.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.webcam_config = config.get('webcam', {})
        self.thresholds = config.get('thresholds', {})
        
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Initialize webcam
        self.cap = None
        self.is_initialized = False
        
        # Tracking state
        self.blink_counter = 0
        self.blink_timestamps = deque(maxlen=20)  # Store last 20 blinks
        self.eye_closed_start = None
        self.ear_threshold = 0.21  # Eye Aspect Ratio threshold for blink
        
        # Face landmark indices for eyes (MediaPipe Face Mesh)
        self.LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
        
        logger.info("FaceTracker initialized")
    
    def initialize(self) -> bool:
        """
        Initialize webcam capture.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            device_id = self.webcam_config.get('device_id', 0)
            self.cap = cv2.VideoCapture(device_id)
            
            if not self.cap.isOpened():
                logger.error(f"Failed to open webcam {device_id}")
                return False
            
            # Set camera properties
            width = self.webcam_config.get('width', 640)
            height = self.webcam_config.get('height', 480)
            fps = self.webcam_config.get('fps', 30)
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.cap.set(cv2.CAP_PROP_FPS, fps)
            
            self.is_initialized = True
            logger.info("Webcam initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing webcam: {e}")
            return False
    
    def get_eye_landmarks(self, landmarks, indices, img_width, img_height):
        """
        Extract eye landmarks as numpy array.
        
        Args:
            landmarks: MediaPipe face landmarks
            indices: List of landmark indices for eye
            img_width: Image width
            img_height: Image height
            
        Returns:
            Numpy array of eye landmark coordinates
        """
        coords = []
        for idx in indices:
            landmark = landmarks[idx]
            x = int(landmark.x * img_width)
            y = int(landmark.y * img_height)
            coords.append([x, y])
        return np.array(coords, dtype=np.float32)
    
    def detect_blinks(self, left_ear, right_ear) -> bool:
        """
        Detect if user is blinking.
        
        Args:
            left_ear: Left eye aspect ratio
            right_ear: Right eye aspect ratio
            
        Returns:
            True if blink detected
        """
        avg_ear = (left_ear + right_ear) / 2.0
        
        if avg_ear < self.ear_threshold:
            # Eye is closed
            if self.eye_closed_start is None:
                self.eye_closed_start = datetime.now()
                self.blink_counter += 1
                self.blink_timestamps.append(datetime.now())
                return True
        else:
            # Eye is open
            self.eye_closed_start = None
        
        return False
    
    def is_drowsy(self) -> bool:
        """
        Determine if user is drowsy based on blink rate and eye closure duration.
        
        Returns:
            True if user appears drowsy
        """
        # Check if eyes have been closed for extended period
        if self.eye_closed_start is not None:
            closed_duration = (datetime.now() - self.eye_closed_start).total_seconds()
            threshold = self.thresholds.get('eye_closed_duration', 2.0)
            if closed_duration > threshold:
                return True
        
        # Check blink rate (blinks per minute)
        if len(self.blink_timestamps) >= 2:
            time_span = (self.blink_timestamps[-1] - self.blink_timestamps[0]).total_seconds()
            if time_span > 0:
                blinks_per_minute = (len(self.blink_timestamps) / time_span) * 60
                threshold = self.thresholds.get('drowsiness_blink_rate', 20)
                if blinks_per_minute > threshold:
                    return True
        
        return False
    
    def estimate_head_pose(self, landmarks, img_width, img_height):
        """
        Estimate head pose angles (pitch, yaw, roll).
        
        Args:
            landmarks: MediaPipe face landmarks
            img_width: Image width
            img_height: Image height
            
        Returns:
            Tuple of (pitch, yaw, roll) in degrees
        """
        # 3D model points (generic face model)
        model_points = np.array([
            (0.0, 0.0, 0.0),             # Nose tip
            (0.0, -330.0, -65.0),        # Chin
            (-225.0, 170.0, -135.0),     # Left eye left corner
            (225.0, 170.0, -135.0),      # Right eye right corner
            (-150.0, -150.0, -125.0),    # Left mouth corner
            (150.0, -150.0, -125.0)      # Right mouth corner
        ], dtype=np.float64)
        
        # 2D image points from landmarks
        image_points = np.array([
            (landmarks[1].x * img_width, landmarks[1].y * img_height),      # Nose tip
            (landmarks[152].x * img_width, landmarks[152].y * img_height),  # Chin
            (landmarks[33].x * img_width, landmarks[33].y * img_height),    # Left eye
            (landmarks[263].x * img_width, landmarks[263].y * img_height),  # Right eye
            (landmarks[61].x * img_width, landmarks[61].y * img_height),    # Left mouth
            (landmarks[291].x * img_width, landmarks[291].y * img_height)   # Right mouth
        ], dtype=np.float64)
        
        # Camera matrix
        focal_length = img_width
        center = (img_width / 2, img_height / 2)
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype=np.float64)
        
        # Assume no lens distortion
        dist_coeffs = np.zeros((4, 1))
        
        # Solve PnP
        success, rotation_vector, translation_vector = cv2.solvePnP(
            model_points, image_points, camera_matrix, dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )
        
        if success:
            # Convert rotation vector to rotation matrix
            rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
            
            # Calculate Euler angles
            pitch = np.arctan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
            yaw = np.arctan2(-rotation_matrix[2, 0],
                           np.sqrt(rotation_matrix[2, 1]**2 + rotation_matrix[2, 2]**2))
            roll = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
            
            # Convert to degrees
            pitch = np.degrees(pitch)
            yaw = np.degrees(yaw)
            roll = np.degrees(roll)
            
            return pitch, yaw, roll
        
        return 0, 0, 0
    
    def is_looking_away(self, yaw, pitch) -> bool:
        """
        Determine if user is looking away from screen.
        
        Args:
            yaw: Head yaw angle
            pitch: Head pitch angle
            
        Returns:
            True if looking away
        """
        angle_threshold = self.thresholds.get('distraction_head_angle', 30)
        return abs(yaw) > angle_threshold or abs(pitch) > angle_threshold
    
    def estimate_gaze_direction(self, landmarks, img_width, img_height):
        """
        Estimate gaze direction based on iris position.
        
        Args:
            landmarks: MediaPipe face landmarks
            img_width: Image width
            img_height: Image height
            
        Returns:
            Gaze deviation score (0 = centered, >0.3 = looking away)
        """
        # Left iris center (landmark 468-473 are iris landmarks with refinement)
        left_iris_x = landmarks[468].x if len(landmarks) > 468 else landmarks[33].x
        left_iris_y = landmarks[468].y if len(landmarks) > 468 else landmarks[33].y
        
        # Right iris center
        right_iris_x = landmarks[473].x if len(landmarks) > 473 else landmarks[263].x
        right_iris_y = landmarks[473].y if len(landmarks) > 473 else landmarks[263].y
        
        # Calculate average iris position
        avg_iris_x = (left_iris_x + right_iris_x) / 2.0
        avg_iris_y = (left_iris_y + right_iris_y) / 2.0
        
        # Calculate deviation from center (0.5, 0.5)
        x_deviation = abs(avg_iris_x - 0.5)
        y_deviation = abs(avg_iris_y - 0.5)
        
        # Combined deviation score
        deviation = np.sqrt(x_deviation**2 + y_deviation**2)
        
        return deviation
    
    def get_attention_state(self) -> AttentionState:
        """
        Determine the current attention state of the user.
        
        Returns:
            AttentionState enum value
        """
        if not self.is_initialized:
            logger.warning("FaceTracker not initialized")
            return AttentionState.DISTRACTED
        
        # Capture frame
        ret, frame = self.cap.read()
        if not ret:
            logger.warning("Failed to capture frame")
            return AttentionState.DISTRACTED
        
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_height, img_width = frame.shape[:2]
        
        # Process with Face Mesh
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            logger.debug("No face detected")
            return AttentionState.DISTRACTED
        
        # Get first face landmarks
        face_landmarks = results.multi_face_landmarks[0].landmark
        
        # Calculate Eye Aspect Ratios
        left_eye_coords = self.get_eye_landmarks(
            face_landmarks, self.LEFT_EYE_INDICES, img_width, img_height
        )
        right_eye_coords = self.get_eye_landmarks(
            face_landmarks, self.RIGHT_EYE_INDICES, img_width, img_height
        )
        
        left_ear = calculate_eye_aspect_ratio(left_eye_coords)
        right_ear = calculate_eye_aspect_ratio(right_eye_coords)
        
        # Detect blinks
        self.detect_blinks(left_ear, right_ear)
        
        # Check for drowsiness
        if self.is_drowsy():
            logger.debug("User appears drowsy")
            return AttentionState.DROWSY
        
        # Estimate head pose
        pitch, yaw, roll = self.estimate_head_pose(face_landmarks, img_width, img_height)
        
        # Check if looking away
        if self.is_looking_away(yaw, pitch):
            logger.debug(f"User looking away (yaw: {yaw:.1f}, pitch: {pitch:.1f})")
            return AttentionState.DISTRACTED
        
        # Estimate gaze direction
        gaze_deviation = self.estimate_gaze_direction(face_landmarks, img_width, img_height)
        gaze_threshold = self.thresholds.get('gaze_deviation_threshold', 0.3)
        
        if gaze_deviation > gaze_threshold:
            logger.debug(f"Gaze deviation too high: {gaze_deviation:.2f}")
            return AttentionState.DISTRACTED
        
        # User is focused
        logger.debug("User is focused")
        return AttentionState.FOCUSED
    
    def release(self):
        """
        Release webcam and cleanup resources.
        """
        if self.cap is not None:
            self.cap.release()
            logger.info("Webcam released")
        self.is_initialized = False


def main():
    """
    Test the FaceTracker module independently.
    """
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Load config
    config = load_config()
    
    # Initialize tracker
    tracker = FaceTracker(config)
    
    if not tracker.initialize():
        print("Failed to initialize webcam!")
        return
    
    print("Face tracker running... Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        while True:
            state = tracker.get_attention_state()
            print(f"\rAttention State: {state.value}     ", end='', flush=True)
            
            # Small delay to prevent overwhelming output
            cv2.waitKey(100)
            
    except KeyboardInterrupt:
        print("\n\nStopping...")
    finally:
        tracker.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
