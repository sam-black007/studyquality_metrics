"""
Activity Decision Engine and Focus Scoring
Combines face state and screen content to determine activity and calculate focus score
"""
from typing import Dict, Tuple
from src.config import (
    FACE_FOCUSED_POINTS, SCREEN_PRODUCTIVE_POINTS,
    FACE_DISTRACTED_PENALTY, FACE_DROWSY_PENALTY,
    SCREEN_DISTRACTION_PENALTY,
    MIN_FOCUS_SCORE, MAX_FOCUS_SCORE
)


class ActivityEngine:
    """
    Decision engine that combines face state and screen classification
    to determine overall activity status
    """
    
    # Decision matrix mapping
    DECISION_MATRIX = {
        # (face_state, screen_class) -> activity_status
        ("FOCUSED", "STUDY"): "PRODUCTIVE",
        ("FOCUSED", "EDUCATIONAL_VIDEO"): "LEARNING",
        ("FOCUSED", "DISTRACTION_VIDEO"): "DISTRACTED",
        ("FOCUSED", "SOCIAL_MEDIA"): "DISTRACTED",
        ("FOCUSED", "OTHER"): "LOW_FOCUS",
        
        ("DISTRACTED", "STUDY"): "LOW_FOCUS",
        ("DISTRACTED", "EDUCATIONAL_VIDEO"): "LOW_FOCUS",
        ("DISTRACTED", "DISTRACTION_VIDEO"): "DISTRACTED",
        ("DISTRACTED", "SOCIAL_MEDIA"): "DISTRACTED",
        ("DISTRACTED", "OTHER"): "DISTRACTED",
        
        ("DROWSY", "STUDY"): "FATIGUED",
        ("DROWSY", "EDUCATIONAL_VIDEO"): "FATIGUED",
        ("DROWSY", "DISTRACTION_VIDEO"): "FATIGUED",
        ("DROWSY", "SOCIAL_MEDIA"): "FATIGUED",
        ("DROWSY", "OTHER"): "FATIGUED",
    }
    
    @staticmethod
    def determine_activity(face_state: str, screen_class: str) -> str:
        """
        Determine activity status based on face state and screen content
        
        Args:
            face_state: "FOCUSED", "DISTRACTED", or "DROWSY"
            screen_class: Screen content class
            
        Returns:
            Activity status: "PRODUCTIVE", "LEARNING", "LOW_FOCUS", "DISTRACTED", "FATIGUED"
        """
        key = (face_state, screen_class)
        return ActivityEngine.DECISION_MATRIX.get(key, "LOW_FOCUS")
    
    @staticmethod
    def is_productive(activity_status: str) -> bool:
        """Check if activity is considered productive"""
        return activity_status in ["PRODUCTIVE", "LEARNING"]
    
    @staticmethod
    def is_distracted(activity_status: str) -> bool:
        """Check if activity is distracted"""
        return activity_status == "DISTRACTED"
    
    @staticmethod
    def is_fatigued(activity_status: str) -> bool:
        """Check if user is fatigued"""
        return activity_status == "FATIGUED"


class FocusScorer:
    """
    Calculates focus score based on face state and screen content
    """
    
    def __init__(self):
        self.current_score = 50  # Start at neutral
    
    def calculate_score(self, face_state: str, screen_class: str) -> int:
        """
        Calculate focus score for current state
        
        Args:
            face_state: "FOCUSED", "DISTRACTED", or "DROWSY"
            screen_class: Screen content class
            
        Returns:
            Focus score (0-100)
        """
        score = 0
        
        # Face state contribution
        if face_state == "FOCUSED":
            score += FACE_FOCUSED_POINTS
        elif face_state == "DISTRACTED":
            score += FACE_DISTRACTED_PENALTY
        elif face_state == "DROWSY":
            score += FACE_DROWSY_PENALTY
        
        # Screen content contribution
        if screen_class in ["STUDY", "EDUCATIONAL_VIDEO"]:
            score += SCREEN_PRODUCTIVE_POINTS
        elif screen_class in ["DISTRACTION_VIDEO", "SOCIAL_MEDIA"]:
            score += SCREEN_DISTRACTION_PENALTY
        
        # Clamp to valid range
        score = max(MIN_FOCUS_SCORE, min(MAX_FOCUS_SCORE, score))
        
        # Update current score (smooth transition)
        self.current_score = int(0.7 * self.current_score + 0.3 * score)
        
        return self.current_score
    
    def get_score_label(self, score: int) -> str:
        """
        Get descriptive label for score
        
        Args:
            score: Focus score (0-100)
            
        Returns:
            Label like "Excellent", "Good", "Fair", "Poor"
        """
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Fair"
        elif score >= 20:
            return "Poor"
        else:
            return "Very Poor"
    
    def reset(self):
        """Reset score to neutral"""
        self.current_score = 50


class FocusAnalyzer:
    """
    Combined analyzer that uses ActivityEngine and FocusScorer
    """
    
    def __init__(self):
        self.engine = ActivityEngine()
        self.scorer = FocusScorer()
    
    def analyze(self, face_state: str, screen_class: str, 
                screen_confidence: float = 1.0) -> Dict:
        """
        Complete analysis of current state
        
        Args:
            face_state: Face attention state
            screen_class: Screen content class
            screen_confidence: Confidence of screen classification
            
        Returns:
            Dictionary with:
                - activity_status: Overall activity status
                - focus_score: Numerical focus score
                - score_label: Descriptive label
                - is_productive: Boolean
        """
        # Determine activity
        activity_status = self.engine.determine_activity(face_state, screen_class)
        
        # Calculate score
        focus_score = self.scorer.calculate_score(face_state, screen_class)
        score_label = self.scorer.get_score_label(focus_score)
        
        # Productivity flag
        is_productive = self.engine.is_productive(activity_status)
        
        return {
            "activity_status": activity_status,
            "focus_score": focus_score,
            "score_label": score_label,
            "is_productive": is_productive,
            "face_state": face_state,
            "screen_class": screen_class,
            "screen_confidence": screen_confidence
        }
    
    def reset(self):
        """Reset analyzer state"""
        self.scorer.reset()
