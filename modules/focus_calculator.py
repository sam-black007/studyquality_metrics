"""
Module 5: Focus Score Calculator

This module calculates a focus score (0-100) based on face attention
and screen content, with smoothing over time.

Author: AI Study Focus Monitor
"""

import logging
from collections import deque
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import AttentionState, ContentCategory, clamp

logger = logging.getLogger(__name__)


class FocusCalculator:
    """
    Calculates focus score based on attention and content.
    """
    
    def __init__(self, config: dict):
        """
        Initialize the focus calculator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        focus_config = config.get('focus', {})
        
        # Smoothing window size (in minutes)
        window_size = focus_config.get('score_smoothing_window', 5)
        self.score_history = deque(maxlen=window_size)
        
        logger.info(f"FocusCalculator initialized (smoothing window: {window_size} min)")
    
    def calculate_score(
        self, 
        face_state: AttentionState, 
        screen_category: ContentCategory
    ) -> int:
        """
        Calculate focus score for current state.
        
        Scoring Algorithm:
        - Base score: 50
        - Face state contribution:
          - FOCUSED: +40
          - DROWSY: -30
          - DISTRACTED: 0 (neutral)
        - Screen content contribution:
          - STUDY or EDUCATIONAL_VIDEO: +30
          - DISTRACTION_VIDEO or SOCIAL_MEDIA: -40
          - OTHER: 0 (neutral)
        - Clamp to [0, 100]
        
        Args:
            face_state: User's attention state
            screen_category: Current screen content category
            
        Returns:
            Focus score (0-100)
        """
        base_score = 50
        score = base_score
        
        # Face state contribution
        if face_state == AttentionState.FOCUSED:
            score += 40
            logger.debug("Score +40 (focused)")
        elif face_state == AttentionState.DROWSY:
            score -= 30
            logger.debug("Score -30 (drowsy)")
        # DISTRACTED: no change
        
        # Screen content contribution
        if screen_category in [ContentCategory.STUDY, ContentCategory.EDUCATIONAL_VIDEO]:
            score += 30
            logger.debug(f"Score +30 ({screen_category.value})")
        elif screen_category in [ContentCategory.DISTRACTION_VIDEO, ContentCategory.SOCIAL_MEDIA]:
            score -= 40
            logger.debug(f"Score -40 ({screen_category.value})")
        # OTHER: no change
        
        # Clamp to valid range
        score = int(clamp(score, 0, 100))
        
        # Add to history
        self.score_history.append(score)
        
        logger.debug(f"Current score: {score}")
        return score
    
    def get_average_score(self) -> int:
        """
        Get the smoothed average score over the recent window.
        
        Returns:
            Average focus score (0-100)
        """
        if not self.score_history:
            return 0
        
        avg = int(sum(self.score_history) / len(self.score_history))
        return avg
    
    def get_current_score(self) -> int:
        """
        Get the most recent score without smoothing.
        
        Returns:
            Current focus score (0-100)
        """
        if not self.score_history:
            return 0
        return self.score_history[-1]
    
    def reset_history(self):
        """
        Reset the score history (useful for starting a new session).
        """
        self.score_history.clear()
        logger.info("Score history reset")


def main():
    """
    Test the FocusCalculator module independently.
    """
    from utils.helpers import load_config
    
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Load config
    config = load_config()
    
    # Initialize calculator
    calculator = FocusCalculator(config)
    
    # Test cases
    test_cases = [
        ("Productive study", AttentionState.FOCUSED, ContentCategory.STUDY, 120),
        ("Learning video", AttentionState.FOCUSED, ContentCategory.EDUCATIONAL_VIDEO, 120),
        ("Distracted while studying", AttentionState.DISTRACTED, ContentCategory.STUDY, 80),
        ("Watching shorts", AttentionState.FOCUSED, ContentCategory.DISTRACTION_VIDEO, 10),
        ("Drowsy", AttentionState.DROWSY, ContentCategory.STUDY, 50),
        ("Social media", AttentionState.DISTRACTED, ContentCategory.SOCIAL_MEDIA, 10),
    ]
    
    print("Focus Score Calculator Test Cases")
    print("=" * 80)
    
    for name, face_state, screen_category, expected_range in test_cases:
        score = calculator.calculate_score(face_state, screen_category)
        avg_score = calculator.get_average_score()
        print(f"{name:30} | Score: {score:3} | Avg: {avg_score:3} | Expected: ~{expected_range}")
    
    print("=" * 80)
    print(f"Final average score: {calculator.get_average_score()}")


if __name__ == "__main__":
    main()
