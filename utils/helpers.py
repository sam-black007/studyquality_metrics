"""
Common helper functions and utilities for the AI Study Focus Monitor.
"""

import yaml
import logging
from pathlib import Path
from datetime import datetime
from enum import Enum


class AttentionState(Enum):
    """Face attention states."""
    FOCUSED = "FOCUSED"
    DISTRACTED = "DISTRACTED"
    DROWSY = "DROWSY"


class ContentCategory(Enum):
    """Screen content categories."""
    STUDY = "STUDY"
    EDUCATIONAL_VIDEO = "EDUCATIONAL_VIDEO"
    DISTRACTION_VIDEO = "DISTRACTION_VIDEO"
    SOCIAL_MEDIA = "SOCIAL_MEDIA"
    OTHER = "OTHER"


class ActivityStatus(Enum):
    """Final activity status combining face and screen data."""
    PRODUCTIVE = "PRODUCTIVE"
    LEARNING = "LEARNING"
    LOW_FOCUS = "LOW_FOCUS"
    DISTRACTED = "DISTRACTED"
    FATIGUED = "FATIGUED"
    NEUTRAL = "NEUTRAL"


def load_config(config_path: str = "config/settings.yaml") -> dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dictionary containing configuration settings
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logging.error(f"Error parsing configuration file: {e}")
        raise


def setup_logging(config: dict) -> None:
    """
    Set up logging configuration.
    
    Args:
        config: Configuration dictionary
    """
    log_level = config.get('logging', {}).get('level', 'INFO')
    log_file = config.get('logging', {}).get('log_file', 'data/app.log')
    
    # Create logs directory if it doesn't exist
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def get_session_id() -> str:
    """
    Generate a unique session ID based on current timestamp.
    
    Returns:
        Session ID string (e.g., '20260205_142530')
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., '2h 15m')
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp a value between min and max.
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))


def calculate_eye_aspect_ratio(eye_points: list) -> float:
    """
    Calculate Eye Aspect Ratio (EAR) for blink detection.
    
    Args:
        eye_points: List of 6 eye landmark points
        
    Returns:
        Eye aspect ratio value
    """
    import numpy as np
    
    # Compute the euclidean distances between the two sets of vertical eye landmarks
    A = np.linalg.norm(eye_points[1] - eye_points[5])
    B = np.linalg.norm(eye_points[2] - eye_points[4])
    
    # Compute the euclidean distance between the horizontal eye landmarks
    C = np.linalg.norm(eye_points[0] - eye_points[3])
    
    # Calculate the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    
    return ear
