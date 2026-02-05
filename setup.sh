#!/bin/bash
# AI Study Focus Monitor - Easy Setup Script for macOS/Linux

echo "========================================"
echo " AI Study Focus Monitor - Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

echo "[OK] Python is installed"
python3 --version
echo ""

# Upgrade pip
echo "[1/4] Upgrading pip..."
python3 -m pip install --upgrade pip --quiet
echo "[OK] pip upgraded"
echo ""

# Install dependencies
echo "[2/4] Installing dependencies (this may take 5-10 minutes)..."
echo "This is downloading TensorFlow, OpenCV, MediaPipe and other libraries..."
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to install some dependencies"
    echo ""
    echo "Common fixes:"
    echo "1. Install development tools: sudo apt-get install python3-dev (Ubuntu/Debian)"
    echo "2. Use a virtual environment: python3 -m venv venv && source venv/bin/activate"
    echo ""
    exit 1
fi
echo "[OK] All dependencies installed"
echo ""

# Create necessary directories
echo "[3/4] Creating data directories..."
mkdir -p data/sessions
mkdir -p data/reports
mkdir -p models
echo "[OK] Directories created"
echo ""

# Test import
echo "[4/4] Verifying installation..."
python3 -c "import cv2, mediapipe, numpy, pandas, matplotlib" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "WARNING: Some imports failed, but you can still try running the app"
else
    echo "[OK] Core libraries verified"
fi
echo ""

echo "========================================"
echo " Installation Complete!"
echo "========================================"
echo ""
echo "To start monitoring, run:"
echo "   python3 main.py"
echo ""
echo "To generate a report, run:"
echo "   python3 -m modules.report_generator"
echo ""
echo "For help, see README.md"
echo ""
