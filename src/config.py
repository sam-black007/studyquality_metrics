"""
Configuration file for AI Study Focus Analyzer
"""
import os

# ============= PATHS =============
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Session logs
SESSION_LOG_CSV = os.path.join(DATA_DIR, "session_log.csv")
SESSION_LOG_JSON = os.path.join(DATA_DIR, "session_log.json")

# Model paths
SCREEN_CLASSIFIER_MODEL = os.path.join(MODELS_DIR, "screen_classifier.h5")

# Training data
TRAINING_DATA_DIR = os.path.join(DATA_DIR, "training_data")

# Reports
REPORTS_DIR = os.path.join(DATA_DIR, "reports")

# ============= FACE TRACKING =============
# Eye Aspect Ratio threshold for drowsiness detection
EAR_THRESHOLD = 0.25
EAR_CONSEC_FRAMES = 3  # Number of consecutive frames below threshold to trigger drowsy

# Gaze detection
GAZE_THRESHOLD = 0.15  # How far eyes can deviate from center

# Head pose thresholds (degrees)
HEAD_PITCH_THRESHOLD = 20  # Looking up/down
HEAD_YAW_THRESHOLD = 25    # Looking left/right

# ============= SCREEN CAPTURE =============
CAPTURE_INTERVAL = 7  # Seconds between screen captures
SCREENSHOT_WIDTH = 224  # Resize for model input
SCREENSHOT_HEIGHT = 224

# ============= CLASSIFICATION =============
# Screen content classes
SCREEN_CLASSES = [
    "STUDY",              # Code editors, PDFs, documentation
    "EDUCATIONAL_VIDEO",  # Long-form learning videos
    "DISTRACTION_VIDEO",  # Shorts, reels, entertainment
    "SOCIAL_MEDIA",       # Social platforms
    "OTHER"               # Unclassified
]

# Classification confidence threshold
CONFIDENCE_THRESHOLD = 0.6

# ============= FOCUS SCORING =============
# Score weights (total should be 100)
FACE_FOCUSED_POINTS = 40
SCREEN_PRODUCTIVE_POINTS = 30
FACE_DISTRACTED_PENALTY = -40
FACE_DROWSY_PENALTY = -30
SCREEN_DISTRACTION_PENALTY = -40

# Score bounds
MIN_FOCUS_SCORE = 0
MAX_FOCUS_SCORE = 100

# ============= ACTIVITY STATES =============
FACE_STATES = ["FOCUSED", "DISTRACTED", "DROWSY"]
ACTIVITY_STATES = ["PRODUCTIVE", "LEARNING", "LOW_FOCUS", "DISTRACTED", "FATIGUED"]

# ============= LOGGING =============
LOG_INTERVAL = 60  # Seconds between log entries (1 minute)

# ============= GUI =============
WINDOW_TITLE = "AI Study Focus Analyzer"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# Webcam display
WEBCAM_DISPLAY_WIDTH = 320
WEBCAM_DISPLAY_HEIGHT = 240

# Pause hotkey
PAUSE_HOTKEY = "ctrl+p"

# ============= REPORTING =============
# Report generation time (24-hour format)
REPORT_GENERATION_HOUR = 23  # 11 PM
REPORT_GENERATION_MINUTE = 59

# Chart settings
CHART_DPI = 100
CHART_FIGSIZE = (10, 6)

# ============= MODEL TRAINING =============
# Training parameters
BATCH_SIZE = 32
EPOCHS = 20
VALIDATION_SPLIT = 0.2
LEARNING_RATE = 0.001

# Data augmentation
USE_DATA_AUGMENTATION = True
ROTATION_RANGE = 10
WIDTH_SHIFT_RANGE = 0.1
HEIGHT_SHIFT_RANGE = 0.1
HORIZONTAL_FLIP = True

# ============= PRIVACY =============
# Never save raw images
SAVE_SCREENSHOTS = False
SAVE_WEBCAM_FRAMES = False

# Only save analysis results
SAVE_ANALYSIS_ONLY = True
