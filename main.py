"""
AI Study Focus Monitor - Main Application

This application monitors your study focus using:
- Webcam-based attention tracking
- Screen content classification
- Real-time focus scoring
- Comprehensive reporting

Author: AI Study Focus Monitor
Version: 1.0.0
"""

import logging
import threading
import time
from datetime import datetime
import sys
import signal

from utils.helpers import (
    load_config,
    setup_logging,
    get_session_id,
    AttentionState,
    ContentCategory,
    ActivityStatus
)

from modules.face_tracker import FaceTracker
from modules.screen_capture import ScreenCapture
from modules.content_classifier import ContentClassifier
from modules.decision_engine import DecisionEngine
from modules.focus_calculator import FocusCalculator
from modules.session_logger import SessionLogger
from modules.dashboard import Dashboard

logger = logging.getLogger(__name__)


class StudyFocusMonitor:
    """
    Main application class that coordinates all modules.
    """
    
    def __init__(self, config: dict):
        """
        Initialize the study focus monitor.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.session_id = get_session_id()
        self.running = False
        self.paused = False
        
        # Initialize all modules
        logger.info("Initializing modules...")
        
        self.face_tracker = FaceTracker(config)
        self.screen_capture = ScreenCapture(config)
        self.content_classifier = ContentClassifier(config)
        self.decision_engine = DecisionEngine(config)
        self.focus_calculator = FocusCalculator(config)
        self.session_logger = SessionLogger(config, self.session_id)
        self.dashboard = Dashboard(config)
        
        # Load ML model
        self.content_classifier.load_model()
        
        # Current state
        self.current_face_state = AttentionState.DISTRACTED
        self.current_screen_category = ContentCategory.OTHER
        self.current_activity_status = ActivityStatus.NEUTRAL
        self.current_focus_score = 0
        
        # Timing
        self.capture_interval = config.get('screen_capture', {}).get('interval_seconds', 7)
        self.log_interval = config.get('focus', {}).get('logging_interval_minutes', 1) * 60
        
        self.last_capture_time = 0
        self.last_log_time = time.time()
        
        logger.info(f"StudyFocusMonitor initialized (Session: {self.session_id})")
    
    def initialize(self) -> bool:
        """
        Initialize hardware components (webcam).
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("Initializing hardware...")
        
        if not self.face_tracker.initialize():
            logger.error("Failed to initialize face tracker")
            return False
        
        logger.info("Hardware initialized successfully")
        return True
    
    def process_frame(self):
        """
        Process a single frame: get face state and update display.
        """
        # Get current face state
        self.current_face_state = self.face_tracker.get_attention_state()
    
    def process_screen_capture(self):
        """
        Capture and classify screen content.
        """
        # Capture screen
        screen_image = self.screen_capture.capture_screen()
        
        # Classify content
        self.current_screen_category = self.content_classifier.classify_screen(screen_image)
    
    def update_status(self):
        """
        Update activity status and focus score based on current data.
        """
        # Determine activity status
        self.current_activity_status = self.decision_engine.determine_activity(
            self.current_face_state,
            self.current_screen_category
        )
        
        # Calculate focus score
        self.current_focus_score = self.focus_calculator.calculate_score(
            self.current_face_state,
            self.current_screen_category
        )
        
        # Update dashboard
        self.dashboard.update_display(
            self.current_face_state,
            self.current_screen_category,
            self.current_focus_score
        )
    
    def log_current_state(self):
        """
        Log the current state to session logger.
        """
        self.session_logger.log_entry(
            self.current_face_state,
            self.current_screen_category,
            self.current_activity_status,
            self.current_focus_score
        )
        
        logger.info(f"Logged: {self.current_activity_status.value} (score: {self.current_focus_score})")
    
    def monitoring_loop(self):
        """
        Main monitoring loop (runs in separate thread).
        """
        logger.info("Monitoring loop started")
        
        while self.running:
            try:
                # Check if paused
                if self.dashboard.is_paused_state():
                    time.sleep(0.5)
                    continue
                
                # Process face tracking (continuous)
                self.process_frame()
                
                # Process screen capture (periodic)
                current_time = time.time()
                if current_time - self.last_capture_time >= self.capture_interval:
                    self.process_screen_capture()
                    self.last_capture_time = current_time
                
                # Update status and display
                self.update_status()
                
                # Log data periodically
                if current_time - self.last_log_time >= self.log_interval:
                    self.log_current_state()
                    self.last_log_time = current_time
                
                # Small delay to prevent overwhelming CPU
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}", exc_info=True)
                time.sleep(1)  # Prevent rapid error loops
        
        logger.info("Monitoring loop stopped")
    
    def start(self):
        """
        Start the study focus monitor.
        """
        logger.info("Starting Study Focus Monitor...")
        
        # Initialize hardware
        if not self.initialize():
            logger.error("Failed to initialize. Exiting.")
            return
        
        # Start monitoring thread
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        # Run dashboard (blocking)
        logger.info("Starting dashboard...")
        try:
            self.dashboard.run()
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
        
        # Cleanup
        self.stop()
    
    def stop(self):
        """
        Stop the study focus monitor and cleanup.
        """
        logger.info("Stopping Study Focus Monitor...")
        
        # Stop monitoring loop
        self.running = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=2)
        
        # Save final log
        self.log_current_state()
        
        # Finalize session
        summary = self.session_logger.finalize_session()
        
        # Release resources
        self.face_tracker.release()
        self.screen_capture.close()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 SESSION SUMMARY")
        print("=" * 60)
        print(f"Duration: {summary['duration_minutes']} minutes")
        print(f"Average Focus Score: {summary['average_focus_score']}/100")
        print(f"\nActivity Breakdown:")
        for activity, count in summary['activity_breakdown'].items():
            print(f"  {activity}: {count} minutes")
        print("=" * 60)
        print(f"\nSession data saved to: data/sessions/session_{self.session_id}.*")
        print("\nThank you for using AI Study Focus Monitor!")
        print("=" * 60)
        
        logger.info("Shutdown complete")


def signal_handler(signum, frame):
    """
    Handle Ctrl+C gracefully.
    """
    print("\n\nReceived interrupt signal. Shutting down...")
    sys.exit(0)


def main():
    """
    Main entry point.
    """
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=" * 60)
    print("🎯 AI Study Focus Monitor v1.0.0")
    print("=" * 60)
    print("\nInitializing system...")
    
    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return
    
    # Setup logging
    setup_logging(config)
    logger.info("=" * 60)
    logger.info("AI Study Focus Monitor Starting")
    logger.info("=" * 60)
    
    # Create and start monitor
    try:
        monitor = StudyFocusMonitor(config)
        monitor.start()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}")
        print("Check data/app.log for details.")


if __name__ == "__main__":
    main()
