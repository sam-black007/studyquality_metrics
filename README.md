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

### Easy Installation (Recommended)

**Windows:**
```bash
git clone https://github.com/sam-black007/studyquality_metrics.git
cd studyquality_metrics
setup.bat
```

**macOS/Linux:**
```bash
git clone https://github.com/sam-black007/studyquality_metrics.git
cd studyquality_metrics
chmod +x setup.sh
./setup.sh
```

The setup script will automatically install all dependencies and set everything up!

### Manual Installation

```bash
git clone https://github.com/sam-black007/studyquality_metrics.git
cd studyquality_metrics
pip install -r requirements.txt
python main.py
```

### Usage

**Start monitoring:**
```bash
python main.py
```

A dashboard will appear showing:
- 👁 Your attention state (Focused/Distracted/Drowsy)
- 🖥 Screen activity category
- 🎯 Real-time focus score (0-100)
- ⏱ Session timer

**Generate report:**
```bash
python -m modules.report_generator
```

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

### Easy Uninstall

**Windows:**
```bash
uninstall.bat
```

**macOS/Linux:**
```bash
chmod +x uninstall.sh
./uninstall.sh
```

The uninstall script will:
- Ask if you want to backup your data
- Remove the application
- Clean up pip installation (if any)

### Manual Uninstall

Simply delete the project folder:
```bash
# Windows
rmdir /s "studyquality_metrics"

# macOS/Linux
rm -rf studyquality_metrics
```

**See [UNINSTALL.md](UNINSTALL.md) for detailed instructions.**

---

## ⚡ Performance Optimization

The app is optimized to prevent CPU/GPU throttling:

✅ **Low CPU Usage:** 15-25% average (target max 40%)  
✅ **No GPU Load:** CPU-only processing by default  
✅ **Optimized Settings:** Reduced FPS (15), frame skipping, longer intervals

**Key optimizations:**
- Processes every 2nd webcam frame (reduces load by 50%)
- Screen capture every 10 seconds (not continuous)
- Image downscaling before ML processing
- Smart sleep delays to prevent continuous 100% CPU

**Customization:**  
Edit `config/settings.yaml` to tune performance for your system.

**See [PERFORMANCE.md](PERFORMANCE.md) for detailed optimization guide.**

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
