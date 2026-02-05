"""
Session Logging Module
Logs activity data to CSV and JSON files
"""
import os
import csv
import json
from datetime import datetime
from typing import Dict, List
from src.config import SESSION_LOG_CSV, SESSION_LOG_JSON, DATA_DIR


class SessionLogger:
    """
    Logs session activity to CSV and JSON files
    """
    
    def __init__(self):
        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # CSV fieldnames
        self.csv_fieldnames = [
            'timestamp',
            'face_state',
            'screen_class',
            'screen_confidence',
            'activity_status',
            'focus_score',
            'score_label',
            'is_productive'
        ]
        
        # Initialize CSV if it doesn't exist
        self._initialize_csv()
        
        # Session data for JSON
        self.session_data = []
        self.session_start_time = datetime.now()
    
    def _initialize_csv(self):
        """Create CSV file with headers if it doesn't exist"""
        if not os.path.exists(SESSION_LOG_CSV):
            with open(SESSION_LOG_CSV, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.csv_fieldnames)
                writer.writeheader()
    
    def log_entry(self, analysis_result: Dict):
        """
        Log a single analysis entry
        
        Args:
            analysis_result: Dictionary from FocusAnalyzer.analyze()
        """
        timestamp = datetime.now().isoformat()
        
        # Prepare entry
        entry = {
            'timestamp': timestamp,
            'face_state': analysis_result.get('face_state', 'UNKNOWN'),
            'screen_class': analysis_result.get('screen_class', 'UNKNOWN'),
            'screen_confidence': analysis_result.get('screen_confidence', 0.0),
            'activity_status': analysis_result.get('activity_status', 'UNKNOWN'),
            'focus_score': analysis_result.get('focus_score', 0),
            'score_label': analysis_result.get('score_label', 'Unknown'),
            'is_productive': analysis_result.get('is_productive', False)
        }
        
        # Append to CSV
        with open(SESSION_LOG_CSV, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.csv_fieldnames)
            writer.writerow(entry)
        
        # Add to session data
        self.session_data.append(entry)
    
    def save_session_json(self):
        """Save session data to JSON file"""
        session_summary = {
            'session_start': self.session_start_time.isoformat(),
            'session_end': datetime.now().isoformat(),
            'total_entries': len(self.session_data),
            'entries': self.session_data
        }
        
        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = SESSION_LOG_JSON.replace('.json', f'_{timestamp}.json')
        
        with open(json_path, 'w') as f:
            json.dump(session_summary, f, indent=2)
        
        print(f"Session data saved to: {json_path}")
        return json_path
    
    def get_session_stats(self) -> Dict:
        """
        Get statistics for current session
        
        Returns:
            Dictionary with session statistics
        """
        if not self.session_data:
            return {
                'total_time': 0,
                'productive_time': 0,
                'distracted_time': 0,
                'avg_focus_score': 0
            }
        
        total_entries = len(self.session_data)
        productive_count = sum(1 for e in self.session_data if e['is_productive'])
        distracted_count = sum(1 for e in self.session_data 
                              if e['activity_status'] == 'DISTRACTED')
        
        avg_score = sum(e['focus_score'] for e in self.session_data) / total_entries
        
        # Assuming each entry represents LOG_INTERVAL seconds
        from src.config import LOG_INTERVAL
        time_per_entry = LOG_INTERVAL / 60  # Convert to minutes
        
        return {
            'total_time': total_entries * time_per_entry,
            'productive_time': productive_count * time_per_entry,
            'distracted_time': distracted_count * time_per_entry,
            'avg_focus_score': avg_score,
            'total_entries': total_entries
        }
    
    def clear_session(self):
        """Clear current session data (for new session)"""
        self.session_data = []
        self.session_start_time = datetime.now()
