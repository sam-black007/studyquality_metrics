"""
Module 4: Activity Decision Engine

This module combines face attention state and screen content category
to determine the user's overall activity status.

Author: AI Study Focus Monitor
"""

import logging
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import AttentionState, ContentCategory, ActivityStatus

logger = logging.getLogger(__name__)


class DecisionEngine:
    """
    Combines face and screen data to determine overall activity status.
    """
    
    def __init__(self, config: dict):
        """
        Initialize the decision engine.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        logger.info("DecisionEngine initialized")
    
    def determine_activity(
        self, 
        face_state: AttentionState, 
        screen_category: ContentCategory
    ) -> ActivityStatus:
        """
        Determine activity status based on face state and screen content.
        
        Decision Matrix:
        - DROWSY + ANY → FATIGUED
        - ANY + DISTRACTION_VIDEO → DISTRACTED
        - ANY + SOCIAL_MEDIA → DISTRACTED
        - DISTRACTED + ANY → DISTRACTED (or LOW_FOCUS if studying)
        - FOCUSED + STUDY → PRODUCTIVE
        - FOCUSED + EDUCATIONAL_VIDEO → LEARNING
        - FOCUSED + OTHER → NEUTRAL
        
        Args:
            face_state: User's attention state
            screen_category: Current screen content category
            
        Returns:
            ActivityStatus enum value
        """
        # Priority 1: Drowsiness overrides everything
        if face_state == AttentionState.DROWSY:
            logger.debug("Activity: FATIGUED (drowsy detected)")
            return ActivityStatus.FATIGUED
        
        # Priority 2: Distracting content overrides attention
        if screen_category in [ContentCategory.DISTRACTION_VIDEO, ContentCategory.SOCIAL_MEDIA]:
            logger.debug(f"Activity: DISTRACTED ({screen_category.value} detected)")
            return ActivityStatus.DISTRACTED
        
        # Priority 3: Distracted face state
        if face_state == AttentionState.DISTRACTED:
            # If studying but distracted, mark as LOW_FOCUS
            if screen_category in [ContentCategory.STUDY, ContentCategory.EDUCATIONAL_VIDEO]:
                logger.debug("Activity: LOW_FOCUS (distracted while studying)")
                return ActivityStatus.LOW_FOCUS
            else:
                logger.debug("Activity: DISTRACTED (not focused)")
                return ActivityStatus.DISTRACTED
        
        # Priority 4: Focused attention
        if face_state == AttentionState.FOCUSED:
            if screen_category == ContentCategory.STUDY:
                logger.debug("Activity: PRODUCTIVE (focused on study)")
                return ActivityStatus.PRODUCTIVE
            elif screen_category == ContentCategory.EDUCATIONAL_VIDEO:
                logger.debug("Activity: LEARNING (focused on educational content)")
                return ActivityStatus.LEARNING
            else:
                logger.debug("Activity: NEUTRAL (focused but unclear content)")
                return ActivityStatus.NEUTRAL
        
        # Default fallback
        logger.debug("Activity: NEUTRAL (default)")
        return ActivityStatus.NEUTRAL


def main():
    """
    Test the DecisionEngine module independently.
    """
    from utils.helpers import load_config
    
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Load config
    config = load_config()
    
    # Initialize engine
    engine = DecisionEngine(config)
    
    # Test cases
    test_cases = [
        (AttentionState.FOCUSED, ContentCategory.STUDY, ActivityStatus.PRODUCTIVE),
        (AttentionState.FOCUSED, ContentCategory.EDUCATIONAL_VIDEO, ActivityStatus.LEARNING),
        (AttentionState.DISTRACTED, ContentCategory.STUDY, ActivityStatus.LOW_FOCUS),
        (AttentionState.DROWSY, ContentCategory.STUDY, ActivityStatus.FATIGUED),
        (AttentionState.FOCUSED, ContentCategory.DISTRACTION_VIDEO, ActivityStatus.DISTRACTED),
        (AttentionState.DISTRACTED, ContentCategory.SOCIAL_MEDIA, ActivityStatus.DISTRACTED),
    ]
    
    print("Decision Engine Test Cases")
    print("=" * 70)
    
    for face_state, screen_category, expected in test_cases:
        result = engine.determine_activity(face_state, screen_category)
        status = "✓" if result == expected else "✗"
        print(f"{status} Face: {face_state.value:12} | Screen: {screen_category.value:20} → {result.value}")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
