@echo off
REM AI Study Focus Analyzer - Windows Uninstall Script
REM This script removes all installed components

echo ============================================================
echo   AI Study Focus Analyzer - Uninstall Wizard
echo ============================================================
echo.

echo WARNING: This will remove the AI Study Focus Analyzer
echo and all its components from your system.
echo.
set /p confirm="Are you sure you want to uninstall? (y/n): "
if /i not "%confirm%"=="y" (
    echo Uninstall cancelled.
    pause
    exit /b 0
)
echo.

REM Remove virtual environment
echo [1/5] Removing virtual environment...
if exist venv (
    rmdir /s /q venv
    echo [OK] Virtual environment removed
) else (
    echo [SKIP] Virtual environment not found
)
echo.

REM Ask about data removal
echo [2/5] User data...
set /p remove_data="Remove training data and session logs? (y/n): "
if /i "%remove_data%"=="y" (
    if exist data (
        rmdir /s /q data
        echo [OK] Data removed
    )
    if exist models (
        rmdir /s /q models
        echo [OK] Models removed
    )
    if exist logs (
        rmdir /s /q logs
        echo [OK] Logs removed
    )
) else (
    echo [SKIP] Data preserved
)
echo.

REM Remove launcher script
echo [3/5] Removing launcher script...
if exist run.bat (
    del run.bat
    echo [OK] Launcher removed
) else (
    echo [SKIP] Launcher not found
)
echo.

REM Remove desktop shortcut
echo [4/5] Removing desktop shortcut...
if exist "%USERPROFILE%\Desktop\AI Study Focus.lnk" (
    del "%USERPROFILE%\Desktop\AI Study Focus.lnk"
    echo [OK] Desktop shortcut removed
) else (
    echo [SKIP] Desktop shortcut not found
)
echo.

REM Final cleanup
echo [5/5] Final cleanup...
if exist __pycache__ rmdir /s /q __pycache__
if exist src\__pycache__ rmdir /s /q src\__pycache__
echo [OK] Cleanup complete
echo.

echo ============================================================
echo   Uninstallation Complete!
echo ============================================================
echo.
echo The AI Study Focus Analyzer has been removed from your system.
echo.
echo To reinstall, run: setup.bat
echo.
echo You can safely delete this folder now if desired.
echo ============================================================
echo.
pause
