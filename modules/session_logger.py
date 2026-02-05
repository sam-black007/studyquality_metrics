"""
Module 6: Session Logger

This module logs study session data to CSV and JSON formats.
NO images or raw data are stored - only metadata (timestamps, states, scores).

Author: AI Study Focus Monitor
"""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import (
    AttentionState, 
    ContentCategory, 
    ActivityStatus,
    get_session_id
)

logger = logging.getLogger(__name__)


class SessionLogger:
    """
    Logs session data in privacy-preserving format.
    """
    
    def __init__(self, config: dict, session_id: str = None):
        """
        Initialize the session logger.
        
        Args:
            config: Configuration dictionary
            session_id: Optional session ID (auto-generated if not provided)
        """
        self.config = config
        self.session_id = session_id or get_session_id()
        self.entries = []
        
        # Create session directory
        self.data_dir = Path("data/sessions")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # File paths
        self.csv_path = self.data_dir / f"session_{self.session_id}.csv"
        self.json_path = self.data_dir / f"session_{self.session_id}.json"
        
        # Initialize CSV file with headers
        self._initialize_csv()
        
        logger.info(f"SessionLogger initialized (ID: {self.session_id})")
    
    def _initialize_csv(self):
        """
        Create CSV file with headers.
        """
        try:
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp',
                    'face_state',
                    'screen_category',
                    'activity_status',
                    'focus_score'
                ])
            logger.info(f"CSV file created: {self.csv_path}")
        except Exception as e:
            logger.error(f"Error creating CSV file: {e}")
    
    def log_entry(
        self,
        face_state: AttentionState,
        screen_category: ContentCategory,
        activity_status: ActivityStatus,
        focus_score: int
    ):
        """
        Log a single entry to the session.
        
        Args:
            face_state: User's attention state
            screen_category: Screen content category
            activity_status: Overall activity status
            focus_score: Focus score (0-100)
        """
        timestamp = datetime.now().isoformat()
        
        # Create entry dictionary
        entry = {
            'timestamp': timestamp,
            'face_state': face_state.value,
            'screen_category': screen_category.value,
            'activity_status': activity_status.value,
            'focus_score': focus_score
        }
        
        # Add to in-memory list
        self.entries.append(entry)
        
        # Append to CSV immediately (for real-time access)
        try:
            with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp,
                    face_state.value,
                    screen_category.value,
                    activity_status.value,
                    focus_score
                ])
        except Exception as e:
            logger.error(f"Error writing to CSV: {e}")
        
        logger.debug(f"Logged entry: {activity_status.value} (score: {focus_score})")
    
    def export_json(self):
        """
        Export all session data to JSON file.
        """
        try:
            data = {
                'session_id': self.session_id,
                'start_time': self.entries[0]['timestamp'] if self.entries else None,
                'end_time': self.entries[-1]['timestamp'] if self.entries else None,
                'total_entries': len(self.entries),
                'entries': self.entries
            }
            
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"JSON exported: {self.json_path}")
            
        except Exception as e:
            logger.error(f"Error exporting JSON: {e}")
    
    def get_session_summary(self) -> dict:
        """
        Get a summary of the current session.
        
        Returns:
            Dictionary containing session statistics
        """
        if not self.entries:
            return {
                'session_id': self.session_id,
                'total_entries': 0,
                'duration_minutes': 0,
                'average_focus_score': 0,
                'activity_breakdown': {}
            }
        
        # Calculate statistics
        start_time = datetime.fromisoformat(self.entries[0]['timestamp'])
        end_time = datetime.fromisoformat(self.entries[-1]['timestamp'])
        duration = (end_time - start_time).total_seconds() / 60  # in minutes
        
        # Average focus score
        scores = [e['focus_score'] for e in self.entries]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Activity breakdown
        activity_counts = {}
        for entry in self.entries:
            status = entry['activity_status']
            activity_counts[status] = activity_counts.get(status, 0) + 1
        
        return {
            'session_id': self.session_id,
            'total_entries': len(self.entries),
            'duration_minutes': round(duration, 1),
            'average_focus_score': round(avg_score, 1),
            'activity_breakdown': activity_counts
        }
    
    def finalize_session(self):
        """
        Finalize the session by exporting JSON and logging summary.
        """
        self.export_json()
        summary = self.get_session_summary()
        
        logger.info(f"Session finalized: {summary['total_entries']} entries, "
                   f"{summary['duration_minutes']} minutes, "
                   f"avg score: {summary['average_focus_score']}")
        
        return summary


def main():
    """
    Test the SessionLogger module independently.
    """
    import time
    from utils.helpers import load_config
    
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Load config
    config = load_config()
    
    # Initialize logger
    logger_test = SessionLogger(config)
    
    print(f"Session Logger Test (ID: {logger_test.session_id})")
    print("=" * 50)
    
    # Log some test entries
    test_data = [
        (AttentionState.FOCUSED, ContentCategory.STUDY, ActivityStatus.PRODUCTIVE, 95),
        (AttentionState.FOCUSED, ContentCategory.EDUCATIONAL_VIDEO, ActivityStatus.LEARNING, 90),
        (AttentionState.DISTRACTED, ContentCategory.SOCIAL_MEDIA, ActivityStatus.DISTRACTED, 25),
        (AttentionState.DROWSY, ContentCategory.STUDY, ActivityStatus.FATIGUED, 40),
        (AttentionState.FOCUSED, ContentCategory.STUDY, ActivityStatus.PRODUCTIVE, 100),
    ]
    
    for i, (face, screen, activity, score) in enumerate(test_data, 1):
        logger_test.log_entry(face, screen, activity, score)
        print(f"Entry {i} logged: {activity.value} (score: {score})")
        time.sleep(0.5)  # Small delay to create time differences
    
    # Get and print summary
    print("\n" + "=" * 50)
    summary = logger_test.finalize_session()
    
    print("\nSession Summary:")
    print(f"  Duration: {summary['duration_minutes']} minutes")
    print(f"  Average Score: {summary['average_focus_score']}")
    print(f"  Activity Breakdown:")
    for activity, count in summary['activity_breakdown'].items():
        print(f"    {activity}: {count} entries")
    
    print(f"\nFiles created:")
    print(f"  CSV: {logger_test.csv_path}")
    print(f"  JSON: {logger_test.json_path}")


if __name__ == "__main__":
    main()
