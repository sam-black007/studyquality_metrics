# Quick Start Guide

Get up and running with AI Study Focus Monitor in 3 easy steps!

## 📥 Installation

### Method 1: From GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/study-focus-monitor.git
cd study-focus-monitor

# Run automatic setup
# For Windows:
setup.bat

# For macOS/Linux:
chmod +x setup.sh
./setup.sh
```

### Method 2: Direct Install with pip

```bash
pip install git+https://github.com/yourusername/study-focus-monitor.git
```

### Method 3: Download Standalone Executable

1. Go to [Releases](https://github.com/yourusername/study-focus-monitor/releases)
2. Download `StudyFocusMonitor-v1.0.0-windows.zip`
3. Extract and run `StudyFocusMonitor.exe`

**No Python installation required!**

---

## 🚀 Usage

### Start Monitoring

```bash
python main.py
```

A dashboard window will appear showing:
- 👁 Your attention state (Focused/Distracted/Drowsy)
- 🖥 What's on your screen (Study/Video/Social Media)
- 🎯 Real-time focus score (0-100)
- ⏱ Session timer

### Using the Dashboard

- **Study** with the monitor running in the background
- **Pause** when you take a break (button or Ctrl+Shift+P)
- **End Session** when done studying
- **View summary** showing your productivity stats

### Generate Report

After a study session:

```bash
python -m modules.report_generator
```

This creates visualizations and insights in `data/reports/`:
- 📊 Time distribution pie chart
- 📈 Focus score timeline
- ⏰ Hourly productivity breakdown
- 📝 Text summary with recommendations

---

## ⚙️ Configuration

Edit `config/settings.yaml` to customize:

```yaml
# Change capture interval (default: 7 seconds)
screen_capture:
  interval_seconds: 10

# Adjust drowsiness threshold
thresholds:
  drowsiness_blink_rate: 25  # blinks per minute
  
# Change keyboard shortcuts
hotkeys:
  pause_resume: "ctrl+shift+p"
```

---

## 🔒 Privacy

✅ **Everything runs offline** - no internet connection needed
✅ **No images saved** - only metadata (timestamps, states, scores)
✅ **Your data stays local** - stored in `data/` folder

---

## 🆘 Troubleshooting

### Webcam not working
- Check that your webcam is connected
- Close other apps using the webcam
- Try changing `device_id` in `config/settings.yaml`

### Installation errors (Windows)
- Enable Long Paths: [Guide](https://pip.pypa.io/warnings/enable-long-paths)
- Run `setup.bat` as Administrator
- Install [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### Low performance
- Increase `screen_capture.interval_seconds` in config
- Close other resource-intensive applications

---

## 📖 Full Documentation

For detailed information, see [README.md](README.md)

---

## 💡 Tips for Best Results

1. ✨ **Good lighting** - Keep your face well-lit
2. 📷 **Position webcam** - Face the camera while studying
3. ⏰ **Regular breaks** - Follow the Pomodoro technique (25min work, 5min break)
4. 📊 **Review reports** - Check daily insights to optimize your schedule
5. 🎯 **Set goals** - Aim for average focus score >70

---

## 🗑️ Uninstallation

### Quick Removal

**If you cloned/downloaded:**
Just delete the project folder!

**If you used pip install:**
```bash
pip uninstall study-focus-monitor
```

### Keep Your Data

Before removing, copy your reports:
```bash
# Your study reports are in:
data/reports/
```

---

## 🤝 Support

- 📧 Email: your.email@example.com
- 🐛 Report bugs: [GitHub Issues](https://github.com/yourusername/study-focus-monitor/issues)
- ⭐ Star the repo if you find it useful!

---

**Happy studying! Stay focused and achieve your goals! 🎯📚**
