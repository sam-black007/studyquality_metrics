"""
Module 2: Screen Capture

This module captures screenshots of the user's screen at regular intervals
for content analysis. All captures are processed in-memory and never saved to disk.

Author: AI Study Focus Monitor
"""

import mss
import numpy as np
from PIL import Image
import logging
import time
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import load_config

logger = logging.getLogger(__name__)


class ScreenCapture:
    """
    Captures screen content for analysis without saving to disk.
    """
    
    def __init__(self, config: dict):
        """
        Initialize the screen capture module.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.capture_config = config.get('screen_capture', {})
        self.interval = self.capture_config.get('interval_seconds', 7)
        self.monitor_index = self.capture_config.get('monitor_index', 0)
        
        # Initialize mss
        self.sct = mss.mss()
        
        # Get monitor information
        self.monitors = self.sct.monitors
        if self.monitor_index >= len(self.monitors):
            logger.warning(f"Monitor index {self.monitor_index} not found, using primary monitor")
            self.monitor_index = 1  # Index 0 is all monitors combined, 1 is primary
        
        logger.info(f"ScreenCapture initialized for monitor {self.monitor_index}")
        logger.info(f"Available monitors: {len(self.monitors) - 1}")  # -1 because index 0 is combined
    
    def capture_screen(self) -> Image.Image:
        """
        Capture the current screen content.
        
        Returns:
            PIL Image object of the screen capture
        """
        try:
            # Capture the specified monitor
            monitor = self.monitors[self.monitor_index]
            screenshot = self.sct.grab(monitor)
            
            # Convert to PIL Image
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            
            logger.debug(f"Screen captured: {img.size}")
            return img
            
        except Exception as e:
            logger.error(f"Error capturing screen: {e}")
            # Return a blank image as fallback
            return Image.new('RGB', (640, 480), color='black')
    
    def capture_as_numpy(self) -> np.ndarray:
        """
        Capture screen and return as numpy array (useful for ML models).
        
        Returns:
            Numpy array (height, width, 3) in RGB format
        """
        img = self.capture_screen()
        return np.array(img)
    
    def get_interval(self) -> int:
        """
        Get the configured capture interval.
        
        Returns:
            Interval in seconds
        """
        return self.interval
    
    def close(self):
        """
        Clean up resources.
        """
        if hasattr(self, 'sct'):
            self.sct.close()
            logger.info("ScreenCapture closed")


def main():
    """
    Test the ScreenCapture module independently.
    """
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Load config
    config = load_config()
    
    # Initialize screen capture
    capture = ScreenCapture(config)
    
    print(f"Screen capture running with {capture.interval}s interval...")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        for i in range(5):  # Capture 5 times for testing
            img = capture.capture_screen()
            print(f"Capture {i+1}: Size={img.size}, Mode={img.mode}")
            time.sleep(capture.interval)
            
    except KeyboardInterrupt:
        print("\n\nStopping...")
    finally:
        capture.close()


if __name__ == "__main__":
    main()
