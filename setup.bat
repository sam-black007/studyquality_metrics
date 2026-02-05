@echo off
REM AI Study Focus Monitor - Easy Setup Script for Windows
REM This script automates the installation process

echo ========================================
echo  AI Study Focus Monitor - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Detected Python version: %PYTHON_VERSION%
echo.

REM Upgrade pip
echo [1/4] Upgrading pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo WARNING: Could not upgrade pip, continuing anyway...
) else (
    echo [OK] pip upgraded
)
echo.

REM Install dependencies
echo [2/4] Installing dependencies (this may take 5-10 minutes)...
echo This is downloading TensorFlow, OpenCV, MediaPipe and other libraries...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install some dependencies
    echo.
    echo Common fixes:
    echo 1. Enable Windows Long Path support: https://pip.pypa.io/warnings/enable-long-paths
    echo 2. Run this script as Administrator
    echo 3. Install Visual C++ Redistributable if prompted
    echo.
    pause
    exit /b 1
)
echo [OK] All dependencies installed
echo.

REM Create necessary directories
echo [3/4] Creating data directories...
if not exist "data\sessions" mkdir data\sessions
if not exist "data\reports" mkdir data\reports
if not exist "models" mkdir models
echo [OK] Directories created
echo.

REM Test import
echo [4/4] Verifying installation...
python -c "import cv2, mediapipe, numpy, pandas, matplotlib" 2>nul
if errorlevel 1 (
    echo WARNING: Some imports failed, but you can still try running the app
) else (
    echo [OK] Core libraries verified
)
echo.

echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo To start monitoring, run:
echo    python main.py
echo.
echo To generate a report, run:
echo    python -m modules.report_generator
echo.
echo For help, see README.md
echo.
pause
