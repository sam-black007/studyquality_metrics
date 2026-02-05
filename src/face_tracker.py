"""
Face & Attention Tracking Module
Uses MediaPipe Face Mesh to detect attention state
"""
import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple, Dict
from src.config import (
    EAR_THRESHOLD, EAR_CONSEC_FRAMES,
    GAZE_THRESHOLD, HEAD_PITCH_THRESHOLD, HEAD_YAW_THRESHOLD
)


class FaceTracker:
    """
    Tracks face attention using webcam.
    Detects: FOCUSED, DISTRACTED, DROWSY states
    """
    
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Drowsiness detection
        self.ear_frames_below_threshold = 0
        
        # Eye landmarks for EAR calculation
        self.LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
        
    def calculate_ear(self, eye_landmarks: np.ndarray) -> float:
        """
        Calculate Eye Aspect Ratio (EAR) for drowsiness detection
        
        Args:
            eye_landmarks: Array of 6 eye landmark points
            
        Returns:
            EAR value (lower = more closed)
        """
        # Vertical distances
        A = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
        B = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
        
        # Horizontal distance
        C = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])
        
        # EAR formula
        ear = (A + B) / (2.0 * C)
        return ear
    
    def get_eye_landmarks(self, landmarks, indices: list, img_w: int, img_h: int) -> np.ndarray:
        """Extract eye landmark coordinates"""
        coords = []
        for idx in indices:
            landmark = landmarks[idx]
            x = int(landmark.x * img_w)
            y = int(landmark.y * img_h)
            coords.append([x, y])
        return np.array(coords)
    
    def estimate_head_pose(self, landmarks, img_w: int, img_h: int) -> Tuple[float, float, float]:
        """
        Estimate head pose angles (pitch, yaw, roll)
        
        Returns:
            (pitch, yaw, roll) in degrees
        """
        # Key facial landmarks for pose estimation
        # Nose tip, chin, left eye corner, right eye corner, left mouth, right mouth
        image_points = np.array([
            (landmarks[1].x * img_w, landmarks[1].y * img_h),      # Nose tip
            (landmarks[152].x * img_w, landmarks[152].y * img_h),  # Chin
            (landmarks[33].x * img_w, landmarks[33].y * img_h),    # Left eye corner
            (landmarks[263].x * img_w, landmarks[263].y * img_h),  # Right eye corner
            (landmarks[61].x * img_w, landmarks[61].y * img_h),    # Left mouth
            (landmarks[291].x * img_w, landmarks[291].y * img_h)   # Right mouth
        ], dtype="double")
        
        # 3D model points (generic face model)
        model_points = np.array([
            (0.0, 0.0, 0.0),             # Nose tip
            (0.0, -330.0, -65.0),        # Chin
            (-225.0, 170.0, -135.0),     # Left eye corner
            (225.0, 170.0, -135.0),      # Right eye corner
            (-150.0, -150.0, -125.0),    # Left mouth
            (150.0, -150.0, -125.0)      # Right mouth
        ])
        
        # Camera internals
        focal_length = img_w
        center = (img_w / 2, img_h / 2)
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype="double")
        
        dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
        
        # Solve PnP
        success, rotation_vector, translation_vector = cv2.solvePnP(
            model_points, image_points, camera_matrix, dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )
        
        # Convert rotation vector to rotation matrix
        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
        
        # Extract angles
        pitch = np.degrees(np.arctan2(rotation_matrix[2][1], rotation_matrix[2][2]))
        yaw = np.degrees(np.arctan2(-rotation_matrix[2][0], 
                                     np.sqrt(rotation_matrix[2][1]**2 + rotation_matrix[2][2]**2)))
        roll = np.degrees(np.arctan2(rotation_matrix[1][0], rotation_matrix[0][0]))
        
        return pitch, yaw, roll
    
    def estimate_gaze(self, landmarks, img_w: int, img_h: int) -> Tuple[float, float]:
        """
        Estimate gaze direction (simplified)
        
        Returns:
            (horizontal_deviation, vertical_deviation) normalized to [-1, 1]
        """
        # Use iris landmarks (468-477 are iris landmarks in refined mesh)
        # Simplified: use eye center vs face center
        
        left_eye_center = np.array([
            landmarks[33].x * img_w,
            landmarks[33].y * img_h
        ])
        
        right_eye_center = np.array([
            landmarks[263].x * img_w,
            landmarks[263].y * img_h
        ])
        
        eyes_center = (left_eye_center + right_eye_center) / 2
        
        # Face center (nose tip)
        face_center = np.array([
            landmarks[1].x * img_w,
            landmarks[1].y * img_h
        ])
        
        # Calculate deviation
        deviation = (eyes_center - face_center) / img_w
        
        return deviation[0], deviation[1]
    
    def analyze_frame(self, frame: np.ndarray) -> Dict:
        """
        Analyze a single frame for attention state
        
        Args:
            frame: BGR image from webcam
            
        Returns:
            Dictionary with:
                - state: "FOCUSED", "DISTRACTED", or "DROWSY"
                - ear: Eye aspect ratio
                - gaze: (horizontal, vertical) deviation
                - head_pose: (pitch, yaw, roll)
                - face_detected: bool
        """
        img_h, img_w = frame.shape[:2]
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return {
                "state": "DISTRACTED",
                "ear": 0.0,
                "gaze": (0.0, 0.0),
                "head_pose": (0.0, 0.0, 0.0),
                "face_detected": False
            }
        
        landmarks = results.multi_face_landmarks[0].landmark
        
        # Calculate EAR for both eyes
        left_eye = self.get_eye_landmarks(landmarks, self.LEFT_EYE_INDICES, img_w, img_h)
        right_eye = self.get_eye_landmarks(landmarks, self.RIGHT_EYE_INDICES, img_w, img_h)
        
        left_ear = self.calculate_ear(left_eye)
        right_ear = self.calculate_ear(right_eye)
        avg_ear = (left_ear + right_ear) / 2.0
        
        # Check for drowsiness
        if avg_ear < EAR_THRESHOLD:
            self.ear_frames_below_threshold += 1
        else:
            self.ear_frames_below_threshold = 0
        
        is_drowsy = self.ear_frames_below_threshold >= EAR_CONSEC_FRAMES
        
        # Estimate head pose
        pitch, yaw, roll = self.estimate_head_pose(landmarks, img_w, img_h)
        
        # Estimate gaze
        gaze_h, gaze_v = self.estimate_gaze(landmarks, img_w, img_h)
        
        # Determine state
        if is_drowsy:
            state = "DROWSY"
        elif abs(yaw) > HEAD_YAW_THRESHOLD or abs(pitch) > HEAD_PITCH_THRESHOLD:
            state = "DISTRACTED"
        elif abs(gaze_h) > GAZE_THRESHOLD or abs(gaze_v) > GAZE_THRESHOLD:
            state = "DISTRACTED"
        else:
            state = "FOCUSED"
        
        return {
            "state": state,
            "ear": avg_ear,
            "gaze": (gaze_h, gaze_v),
            "head_pose": (pitch, yaw, roll),
            "face_detected": True
        }
    
    def draw_debug_info(self, frame: np.ndarray, analysis: Dict) -> np.ndarray:
        """
        Draw debug information on frame
        
        Args:
            frame: Original frame
            analysis: Analysis result from analyze_frame
            
        Returns:
            Frame with debug overlay
        """
        annotated = frame.copy()
        
        # State indicator
        state = analysis["state"]
        color = {
            "FOCUSED": (0, 255, 0),      # Green
            "DISTRACTED": (0, 165, 255),  # Orange
            "DROWSY": (0, 0, 255)         # Red
        }.get(state, (255, 255, 255))
        
        cv2.putText(annotated, f"State: {state}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        # EAR
        cv2.putText(annotated, f"EAR: {analysis['ear']:.2f}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Head pose
        pitch, yaw, roll = analysis["head_pose"]
        cv2.putText(annotated, f"Pitch: {pitch:.1f} Yaw: {yaw:.1f}", (10, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return annotated
    
    def release(self):
        """Release resources"""
        self.face_mesh.close()
