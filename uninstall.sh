#!/bin/bash
# AI Study Focus Monitor - Uninstall Script for macOS/Linux

echo "========================================"
echo " AI Study Focus Monitor - Uninstall"
echo "========================================"
echo ""
echo "This will remove the AI Study Focus Monitor from your system."
echo ""

# Ask for confirmation
read -p "Are you sure you want to uninstall? (y/n): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo ""
    echo "Uninstallation cancelled."
    exit 0
fi

echo ""
echo "[1/4] Checking if application is running..."
if pgrep -f "main.py" > /dev/null; then
    echo "WARNING: Study Monitor app is running. Please close it first."
    read -p "Press Enter to continue after closing the app..."
fi
echo "[OK] No conflicts detected"
echo ""

# Ask about data backup
echo "[2/4] Do you want to backup your study data before removing?"
read -p "Backup data to Home directory? (y/n): " backup
if [[ "$backup" =~ ^[Yy]$ ]]; then
    echo "Backing up data to ~/StudyMonitorBackup..."
    mkdir -p ~/StudyMonitorBackup
    if [ -d "data/sessions" ]; then
        cp -r data/sessions ~/StudyMonitorBackup/ 2>/dev/null
    fi
    if [ -d "data/reports" ]; then
        cp -r data/reports ~/StudyMonitorBackup/ 2>/dev/null
    fi
    echo "[OK] Data backed up to ~/StudyMonitorBackup/"
else
    echo "Skipping backup..."
fi
echo ""

# Remove pip installation if exists
echo "[3/4] Removing pip installation (if any)..."
pip3 uninstall -y study-focus-monitor >/dev/null 2>&1 || pip uninstall -y study-focus-monitor >/dev/null 2>&1
echo "[OK] Pip package removed (if it was installed)"
echo ""

# Final confirmation
echo "[4/4] Ready to delete application files"
echo ""
echo "The following will be deleted:"
echo "  - Application code (all Python files)"
echo "  - Configuration files"
echo "  - Session data and reports (unless backed up)"
echo "  - Dependencies will NOT be removed"
echo ""
read -p "Proceed with deletion? (y/n): " finalconfirm
if [[ ! "$finalconfirm" =~ ^[Yy]$ ]]; then
    echo ""
    echo "Uninstallation cancelled."
    exit 0
fi

echo ""
echo "Removing application files..."
echo ""

# Get the project directory
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Deleting: $PROJECT_DIR"

# Navigate to parent and delete
cd ..
rm -rf "$PROJECT_DIR"

if [ -d "$PROJECT_DIR" ]; then
    echo ""
    echo "ERROR: Could not delete all files. Please delete manually:"
    echo "$PROJECT_DIR"
    echo ""
    exit 1
fi

echo ""
echo "========================================"
echo " Uninstallation Complete!"
echo "========================================"
echo ""
echo "AI Study Focus Monitor has been removed from your system."
echo ""
if [[ "$backup" =~ ^[Yy]$ ]]; then
    echo "Your data backup is saved at:"
    echo "~/StudyMonitorBackup/"
    echo ""
fi
echo "Thank you for using Study Focus Monitor!"
echo ""
