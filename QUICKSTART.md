# Quick Start Guide

## First-Time Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Collect Training Data
```bash
python collect_data.py
```

**Instructions:**
1. Select class 1 (STUDY)
2. Open study materials (PDFs, code editors, documentation)
3. Let it capture 50 samples (takes ~3 minutes)
4. Repeat for other classes:
   - Class 2: EDUCATIONAL_VIDEO (YouTube lectures, tutorials)
   - Class 3: DISTRACTION_VIDEO (shorts, reels, entertainment)
   - Class 4: SOCIAL_MEDIA (Twitter, Instagram, etc.)
   - Class 5: OTHER (anything else)

**Tip:** More diverse samples = better accuracy!

### Step 3: Train the Model
```bash
python train_model.py
```

This takes 5-10 minutes. The model will be saved to `models/screen_classifier.h5`.

### Step 4: Run the Application
```bash
python main.py
```

## Daily Usage

1. **Launch**: `python main.py`
2. **Start**: Click "Start Monitoring"
3. **Pause**: Press `Ctrl+P` anytime
4. **Stop**: Click "Stop" when done
5. **Report**: Click "Generate Report" to see your productivity summary

## Troubleshooting

### Webcam not working
- Check if another app is using the webcam
- Grant camera permissions to Python

### Model accuracy is poor
- Collect more training samples (100+ per class recommended)
- Ensure diverse examples in training data
- Retrain the model

### High CPU usage
- Increase `CAPTURE_INTERVAL` in `src/config.py`
- Reduce webcam resolution

## Tips for Best Results

1. **Good lighting** helps face tracking accuracy
2. **Position webcam** at eye level
3. **Collect diverse training data** from different times of day
4. **Review reports** to understand your productivity patterns
