#!/bin/bash
# AI Study Focus Analyzer - Unix Setup Script
# This script automates the installation process

echo "============================================================"
echo "  AI Study Focus Analyzer - Setup Wizard"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  - Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  - macOS: brew install python3"
    echo "  - Fedora: sudo dnf install python3"
    exit 1
fi

echo "[OK] Python found"
python3 --version
echo ""

# Create virtual environment
echo "[1/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment!"
        exit 1
    fi
    echo "[OK] Virtual environment created"
fi
echo ""

# Activate virtual environment and install dependencies
echo "[2/5] Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies!"
    exit 1
fi
echo "[OK] Dependencies installed"
echo ""

# Create necessary directories
echo "[3/5] Creating project directories..."
mkdir -p data/training_data
mkdir -p data/reports
mkdir -p models
mkdir -p logs
echo "[OK] Directories created"
echo ""

# Create run script
echo "[4/5] Creating launcher script..."
cat > run.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python3 main.py
EOF
chmod +x run.sh
echo "[OK] Launcher created (run.sh)"
echo ""

# Final instructions
echo "[5/5] Setup complete!"
echo ""
echo "============================================================"
echo "  Installation Successful!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  1. Run: python3 collect_data.py  (to collect training samples)"
echo "  2. Run: python3 train_model.py   (to train the ML model)"
echo "  3. Run: ./run.sh                 (to start the application)"
echo ""
echo "To uninstall, run: ./uninstall.sh"
echo "============================================================"
echo ""
