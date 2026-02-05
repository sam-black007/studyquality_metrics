# AI Study Focus & Screen Activity Analyzer

A local desktop AI system that monitors study focus using webcam-based face tracking and screen content analysis.

## 🎯 Features

- **Face & Attention Tracking**: Detects if you're focused, distracted, or drowsy using your webcam
- **Screen Content Classification**: Analyzes what's on your screen (study materials, videos, social media)
- **Focus Score Calculation**: Real-time focus score (0-100) based on attention and screen content
- **Session Logging**: Tracks your activity throughout the day
- **Daily Reports**: Generates productivity summaries with charts and insights
- **Live Dashboard**: Real-time monitoring interface

## 🔒 Privacy

- **100% Local**: Everything runs on your machine
- **No Cloud APIs**: No data leaves your computer
- **No Image Storage**: Only analysis data is saved, not screenshots or webcam images
- **Pause Anytime**: Keyboard shortcut to pause monitoring

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Collect Training Data (First Time Only)

```bash
python collect_data.py
```

Follow the prompts to capture examples of "Study" and "Distraction" screens. Collect at least 50 samples per class.

### 3. Train the Model (First Time Only)

```bash
python train_model.py
```

This will train a MobileNetV2 model on your collected data.

### 4. Run the Application

```bash
python main.py
```

## 📊 How It Works

1. **Webcam** monitors your face for attention signals (gaze, drowsiness, head pose)
2. **Screen capture** analyzes what you're viewing every 5-10 seconds
3. **ML classifier** categorizes screen content into Study/Educational/Distraction
4. **Decision engine** combines face + screen data
5. **Focus score** updates in real-time (0-100)
6. **Logger** saves activity data every minute
7. **Reporter** generates daily summaries with charts

## 🛠 Tech Stack

- **OpenCV** & **MediaPipe**: Face tracking and pose estimation
- **mss**: Efficient screen capture
- **TensorFlow**: ML classification with MobileNetV2
- **Pandas** & **Matplotlib**: Data analysis and visualization
- **Tkinter**: GUI dashboard

## 📁 Project Structure

```
project_root/
├── data/           # Session logs and training data
├── models/         # Trained ML models
├── logs/           # Application logs
├── src/            # Source code modules
│   ├── config.py
│   ├── face_tracker.py
│   ├── screen_eye.py
│   ├── logic.py
│   ├── logger.py
│   ├── reporter.py
│   └── gui.py
├── main.py         # Application entry point
├── train_model.py  # Model training script
└── collect_data.py # Data collection tool
```

## 🎮 Usage

- **Start Monitoring**: Click "Start" in the dashboard
- **Pause**: Press `Ctrl+P` or click "Pause"
- **Stop**: Click "Stop" to end session
- **View Reports**: Check `data/reports/` folder or click "Generate Report"
- **Session Logs**: See `data/session_log.csv`

## 📈 Understanding Your Reports

- **Productive Time**: Study materials + educational videos
- **Distraction Time**: Social media, short-form videos
- **Focus Score**: Average attention level (higher is better)
- **Peak Hours**: When you're most focused

## ⚙️ Configuration

Edit `src/config.py` to customize:
- Screenshot interval
- Focus score weights
- Classification thresholds
- Report generation schedule

## 🤝 Contributing

This is a personal productivity tool. Feel free to fork and customize for your needs!

## 📄 License

MIT License - See LICENSE file for details
