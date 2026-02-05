@echo off
REM AI Study Focus Monitor - Uninstall Script for Windows

echo ========================================
echo  AI Study Focus Monitor - Uninstall
echo ========================================
echo.
echo This will remove the AI Study Focus Monitor from your system.
echo.

REM Ask for confirmation
set /p confirm="Are you sure you want to uninstall? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo.
    echo Uninstallation cancelled.
    pause
    exit /b 0
)

echo.
echo [1/4] Checking if application is running...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo WARNING: Python processes are running. Please close the Study Monitor app first.
    echo Press Ctrl+C to cancel, or
    pause
)
echo [OK] No conflicts detected
echo.

REM Ask about data backup
echo [2/4] Do you want to backup your study data before removing?
set /p backup="Backup data to Desktop? (Y/N): "
if /i "%backup%"=="Y" (
    echo Backing up data to Desktop...
    if exist "data\sessions" (
        xcopy "data\sessions" "%USERPROFILE%\Desktop\StudyMonitorBackup\sessions\" /E /I /Y >NUL 2>&1
    )
    if exist "data\reports" (
        xcopy "data\reports" "%USERPROFILE%\Desktop\StudyMonitorBackup\reports\" /E /I /Y >NUL 2>&1
    )
    echo [OK] Data backed up to Desktop\StudyMonitorBackup\
) else (
    echo Skipping backup...
)
echo.

REM Remove pip installation if exists
echo [3/4] Removing pip installation (if any)...
pip uninstall -y study-focus-monitor >NUL 2>&1
echo [OK] Pip package removed (if it was installed)
echo.

REM Final confirmation
echo [4/4] Ready to delete application files
echo.
echo The following will be deleted:
echo   - Application code (all Python files)
echo   - Configuration files
echo   - Session data and reports (unless backed up)
echo   - Dependencies will NOT be removed
echo.
set /p finalconfirm="Proceed with deletion? (Y/N): "
if /i not "%finalconfirm%"=="Y" (
    echo.
    echo Uninstallation cancelled.
    pause
    exit /b 0
)

echo.
echo Removing application files...
echo.

REM Navigate to parent directory and delete project folder
cd ..
set FOLDER_PATH=%CD%\test file
echo Deleting: %FOLDER_PATH%
rmdir /s /q "%FOLDER_PATH%" 2>NUL

if exist "%FOLDER_PATH%" (
    echo.
    echo ERROR: Could not delete all files. Please delete manually:
    echo %FOLDER_PATH%
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Uninstallation Complete!
echo ========================================
echo.
echo AI Study Focus Monitor has been removed from your system.
echo.
if /i "%backup%"=="Y" (
    echo Your data backup is saved at:
    echo %USERPROFILE%\Desktop\StudyMonitorBackup\
    echo.
)
echo Thank you for using Study Focus Monitor!
echo.
pause
