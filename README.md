# AI Study Focus Monitor

A local, offline desktop AI system that monitors your study focus using webcam-based attention tracking and intelligent screen content analysis.

## 🎯 Features

- **Face & Attention Tracking**: Detects whether you're focused, distracted, or drowsy using MediaPipe
- **Screen Content Classification**: Analyzes what's on your screen using ML and heuristics
- **Real-time Focus Scoring**: Calculates a 0-100 focus score combining face and screen data
- **Live Dashboard**: See your current status in real-time with a clean GUI
- **Session Logging**: Privacy-preserving logs (no images stored, only metadata)
- **Daily Reports**: Comprehensive reports with visualizations and insights

## 🔒 Privacy

- Everything runs **100% locally** on your machine
- **No cloud APIs** or external services
- **No images saved** - only metadata (timestamps, states, scores)
- All processing happens in-memory

## 📋 Requirements

- Python 3.10 or higher
- Webcam
- Windows, macOS, or Linux

## 🚀 Quick Start

### Method 1: One-Click Setup (Recommended for Beginners)

**Windows:**
```bash
# 1. Download or clone this repository
git clone https://github.com/yourusername/study-focus-monitor.git
cd study-focus-monitor

# 2. Run the setup script (installs everything automatically)
setup.bat
```

**macOS/Linux:**
```bash
# 1. Download or clone this repository
git clone https://github.com/yourusername/study-focus-monitor.git
cd study-focus-monitor

# 2. Make setup script executable and run
chmod +x setup.sh
./setup.sh
```

The setup script will:
- ✅ Check Python installation
- ✅ Upgrade pip
- ✅ Install all dependencies
- ✅ Create necessary directories
- ✅ Verify installation

### Method 2: Install Directly from GitHub

```bash
pip install git+https://github.com/yourusername/study-focus-monitor.git
```

### Method 3: Manual Installation

If you prefer to install manually:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/study-focus-monitor.git
   cd study-focus-monitor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

### Method 4: Standalone Executable (No Python Required!)

Perfect for users who don't have Python installed:

1. Go to [Releases](https://github.com/yourusername/study-focus-monitor/releases)
2. Download `StudyFocusMonitor-Windows.zip` (or Mac/Linux version)
3. Extract and double-click `StudyFocusMonitor.exe`
4. Done! No installation needed.

> **Note:** First launch may take 30-60 seconds as the app initializes.

## 📁 Project Structure

```
study-focus-monitor/
├── main.py                     # Main application
├── requirements.txt            # Python dependencies
├── config/
│   └── settings.yaml          # Configuration settings
├── modules/
│   ├── face_tracker.py        # Face & attention tracking
│   ├── screen_capture.py      # Screen capture
│   ├── content_classifier.py  # ML classification
│   ├── decision_engine.py     # Activity decision logic
│   ├── focus_calculator.py    # Focus score calculation
│   ├── session_logger.py      # Session logging
│   ├── report_generator.py    # Daily reports
│   └── dashboard.py           # Live GUI dashboard
├── utils/
│   └── helpers.py             # Utility functions
├── data/
│   ├── sessions/              # Session logs (CSV/JSON)
│   ├── reports/               # Generated reports
│   └── app.log                # Application log
└── models/
    └── screen_classifier.h5   # ML model (auto-created)
```

## ⚙️ Configuration

Edit `config/settings.yaml` to customize:

- Webcam settings (device ID, resolution)
- Screen capture interval
- Focus calculation parameters
- Drowsiness thresholds
- Keyboard shortcuts
- And more...

## 🧪 Testing Individual Modules

Each module can be tested independently:

```bash
# Test face tracker
python -m modules.face_tracker

# Test screen capture
python -m modules.screen_capture

# Test content classifier
python -m modules.content_classifier

# Test decision engine
python -m modules.decision_engine

# Test focus calculator
python -m modules.focus_calculator

# Test session logger
python -m modules.session_logger

# Test dashboard
python -m modules.dashboard
```

## 📊 Understanding the Output

### Activity Statuses

- **PRODUCTIVE**: Focused on study materials (code, PDFs, docs)
- **LEARNING**: Focused on educational videos
- **LOW_FOCUS**: Distracted while study content is on screen
- **DISTRACTED**: Not focused, or viewing distracting content
- **FATIGUED**: Drowsy or showing signs of tiredness
- **NEUTRAL**: Focused but unclear content type

### Focus Score (0-100)

- **80-100**: Excellent focus
- **60-79**: Good focus
- **40-59**: Moderate focus
- **20-39**: Low focus
- **0-19**: Very distracted

## 📈 Daily Reports Include

- Total productive study time
- Total distraction time
- Average focus score
- Peak productivity hours
- Time distribution pie chart
- Focus score timeline
- Hourly productivity breakdown
- Actionable insights and recommendations

## 🗑️ Uninstallation

### If Installed via Method 1, 3, or 4 (Cloned/Downloaded)

Simply delete the project folder:

**Windows:**
```bash
# Navigate to parent directory and delete
cd "d:\"
rmdir /s "test file"
```

Or just delete the folder manually in File Explorer.

**macOS/Linux:**
```bash
rm -rf /path/to/study-focus-monitor
```

### If Installed via Method 2 (pip install)

```bash
pip uninstall study-focus-monitor
```

### Removing Data Files

By default, session logs and reports are stored in the `data/` folder. If you want to remove all your data:

**Before uninstalling:**
```bash
# Backup your data (optional)
cp -r data/sessions ~/backup/study-sessions
cp -r data/reports ~/backup/study-reports

# Or just delete everything
rm -rf data/
```

### Clean Uninstall Checklist

- [ ] Stop the application if it's running
- [ ] Backup any reports you want to keep (from `data/reports/`)
- [ ] Delete the project folder
- [ ] (Optional) Uninstall Python dependencies if not used by other projects:
  ```bash
  pip uninstall opencv-python mediapipe tensorflow-cpu pandas matplotlib
  ```

---

## 🛠️ Troubleshooting

### Webcam not detected
- Check that your webcam is connected and not in use
- Try changing `device_id` in `config/settings.yaml`

### Low classification accuracy
- The ML model uses transfer learning and may need fine-tuning
- Rule-based heuristics work well for code editors, PDFs, and YouTube

### High CPU usage
- Increase `screen_capture.interval_seconds` in config
- Lower webcam resolution in config

### Missing dependencies
- Ensure all packages in `requirements.txt` are installed
- Use a virtual environment to avoid conflicts

## 🎓 Tips for Best Results

1. **Good Lighting**: Ensure your face is well-lit for accurate tracking
2. **Face the Camera**: Keep your face visible to the webcam
3. **Regular Breaks**: Take breaks every 25-30 minutes (Pomodoro technique)
4. **Review Reports**: Check daily reports to identify productivity patterns
5. **Adjust Thresholds**: Customize settings in `config/settings.yaml` for your needs

## 🔜 Future Enhancements (Optional)

- Subject type detection (coding vs reading vs video)
- Pomodoro timer integration
- Weekly productivity reports
- App/website usage statistics
- Browser extension for better YouTube detection
- Custom notification system

## 📝 Data Privacy

All data is stored locally in the `data/` directory:
- **Session logs**: CSV and JSON files with timestamps and states
- **Reports**: PNG charts and TXT summaries
- **App logs**: System logs for debugging

**No images or video frames are ever saved to disk.**

## 📄 License

This project is for personal use. Modify and extend as needed.

## 🙏 Acknowledgments

- MediaPipe for face mesh technology
- TensorFlow for ML capabilities
- mss for fast screen capture
- All open-source contributors

---

**Stay focused and achieve your goals! 🎯**
