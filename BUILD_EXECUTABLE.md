# Instructions for Building Standalone Executable

Follow these steps to create a standalone `.exe` file that users can run without installing Python.

## Prerequisites

Install PyInstaller:
```bash
pip install pyinstaller
```

## Build the Executable

### Windows

Run this command in the project root:

```bash
pyinstaller --name="StudyFocusMonitor" ^
    --onefile ^
    --windowed ^
    --icon=icon.ico ^
    --add-data "config;config" ^
    --add-data "models;models" ^
    --hidden-import=mediapipe ^
    --hidden-import=cv2 ^
    --hidden-import=tensorflow ^
    --hidden-import=matplotlib ^
    --hidden-import=pandas ^
    main.py
```

### macOS/Linux

```bash
pyinstaller --name="StudyFocusMonitor" \
    --onefile \
    --windowed \
    --add-data "config:config" \
    --add-data "models:models" \
    --hidden-import=mediapipe \
    --hidden-import=cv2 \
    --hidden-import=tensorflow \
    --hidden-import=matplotlib \
    --hidden-import=pandas \
    main.py
```

## Output

The executable will be created in the `dist/` folder:
- Windows: `dist/StudyFocusMonitor.exe`
- macOS: `dist/StudyFocusMonitor.app`
- Linux: `dist/StudyFocusMonitor`

## Distribution

For distribution, create a zip file containing:
```
StudyFocusMonitor/
├── StudyFocusMonitor.exe  (or .app on macOS)
├── config/
│   └── settings.yaml
├── data/
│   ├── sessions/
│   └── reports/
├── models/
└── README.md
```

## Notes

- The first run may be slow as TensorFlow initializes
- File size will be ~500MB due to TensorFlow inclusion
- For smaller builds, consider removing TensorFlow and using only rule-based classification
- Test the executable on a clean system without Python installed

## Alternative: Lightweight Build

For a smaller executable without ML features:

1. Remove TensorFlow from requirements.txt
2. Modify content_classifier.py to use only rule-based detection
3. Build with PyInstaller (will be ~100MB instead of 500MB)

## Troubleshooting

If the build fails:
1. Make sure all dependencies are installed: `pip install -r requirements.txt`
2. Try building without `--windowed` flag first to see console output
3. Check PyInstaller documentation: https://pyinstaller.org
