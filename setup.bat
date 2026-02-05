@echo off
REM AI Study Focus Analyzer - Windows Setup Script
REM This script automates the installation process

echo ============================================================
echo   AI Study Focus Analyzer - Setup Wizard
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Create virtual environment
echo [1/6] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment and install dependencies
echo [2/6] Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Create necessary directories
echo [3/6] Creating project directories...
if not exist data mkdir data
if not exist data\training_data mkdir data\training_data
if not exist data\reports mkdir data\reports
if not exist models mkdir models
if not exist logs mkdir logs
echo [OK] Directories created
echo.

REM Create run script
echo [4/6] Creating launcher script...
(
echo @echo off
echo call venv\Scripts\activate.bat
echo python main.py
echo pause
) > run.bat
echo [OK] Launcher created (run.bat)
echo.

REM Create desktop shortcut (optional)
echo [5/6] Desktop shortcut...
set /p create_shortcut="Create desktop shortcut? (y/n): "
if /i "%create_shortcut%"=="y" (
    powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\AI Study Focus.lnk'); $Shortcut.TargetPath = '%CD%\run.bat'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.IconLocation = 'shell32.dll,21'; $Shortcut.Save()"
    echo [OK] Desktop shortcut created
) else (
    echo [SKIP] Desktop shortcut skipped
)
echo.

REM Final instructions
echo [6/6] Setup complete!
echo.
echo ============================================================
echo   Installation Successful!
echo ============================================================
echo.
echo Next steps:
echo   1. Run: collect_data.py  (to collect training samples)
echo   2. Run: train_model.py   (to train the ML model)
echo   3. Run: run.bat          (to start the application)
echo.
echo Or double-click "run.bat" to launch the application.
echo.
echo To uninstall, run: uninstall.bat
echo ============================================================
echo.
pause
