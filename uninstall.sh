#!/bin/bash
# AI Study Focus Analyzer - Unix Uninstall Script
# This script removes all installed components

echo "============================================================"
echo "  AI Study Focus Analyzer - Uninstall Wizard"
echo "============================================================"
echo ""

echo "WARNING: This will remove the AI Study Focus Analyzer"
echo "and all its components from your system."
echo ""
read -p "Are you sure you want to uninstall? (y/n): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Uninstall cancelled."
    exit 0
fi
echo ""

# Remove virtual environment
echo "[1/5] Removing virtual environment..."
if [ -d "venv" ]; then
    rm -rf venv
    echo "[OK] Virtual environment removed"
else
    echo "[SKIP] Virtual environment not found"
fi
echo ""

# Ask about data removal
echo "[2/5] User data..."
read -p "Remove training data and session logs? (y/n): " remove_data
if [ "$remove_data" = "y" ] || [ "$remove_data" = "Y" ]; then
    if [ -d "data" ]; then
        rm -rf data
        echo "[OK] Data removed"
    fi
    if [ -d "models" ]; then
        rm -rf models
        echo "[OK] Models removed"
    fi
    if [ -d "logs" ]; then
        rm -rf logs
        echo "[OK] Logs removed"
    fi
else
    echo "[SKIP] Data preserved"
fi
echo ""

# Remove launcher script
echo "[3/5] Removing launcher script..."
if [ -f "run.sh" ]; then
    rm run.sh
    echo "[OK] Launcher removed"
else
    echo "[SKIP] Launcher not found"
fi
echo ""

# Remove Python cache
echo "[4/5] Removing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "[OK] Cache removed"
echo ""

# Final cleanup
echo "[5/5] Final cleanup complete!"
echo ""

echo "============================================================"
echo "  Uninstallation Complete!"
echo "============================================================"
echo ""
echo "The AI Study Focus Analyzer has been removed from your system."
echo ""
echo "To reinstall, run: ./setup.sh"
echo ""
echo "You can safely delete this folder now if desired."
echo "============================================================"
echo ""
