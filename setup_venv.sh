#!/bin/bash
# Setup script for AutoTune virtual environment

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install the package in development mode
echo "Installing AutoTune in development mode..."
pip install -e .

# Try to install Coqui TTS if Python version is compatible
PYTHON_VERSION=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Detected Python version: $PYTHON_VERSION"

if python -c "import sys; exit(0 if (sys.version_info >= (3, 9) and sys.version_info < (3, 12)) else 1)"; then
    echo "Python version is compatible with Coqui TTS. Installing..."
    pip install git+https://github.com/coqui-ai/TTS.git || echo "Failed to install Coqui TTS. The library will run in simulation mode."
else
    echo "Python version $PYTHON_VERSION is not compatible with Coqui TTS (requires 3.9-3.11)."
    echo "AutoTune will run in simulation mode without actual TTS functionality."
    echo "To use full functionality, create a virtual environment with Python 3.9-3.11."
fi

echo ""
echo "Setup complete! Virtual environment is now active."
echo "To deactivate the virtual environment, run: deactivate"
echo ""
echo "To use AutoTune, you can:"
echo "1. Run the example: python examples/basic_usage.py"
echo "2. Use the CLI: python app/app.py --help"
echo ""