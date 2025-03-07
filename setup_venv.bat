@echo off
REM Setup script for AutoTune virtual environment on Windows

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Install the package in development mode
echo Installing AutoTune in development mode...
pip install -e .

REM Try to install Coqui TTS if Python version is compatible
echo Checking Python version...
python -c "import sys; print(f'Detected Python version: {sys.version_info.major}.{sys.version_info.minor}')"

python -c "import sys; exit(0 if (sys.version_info >= (3, 9) and sys.version_info < (3, 12)) else 1)"
if %ERRORLEVEL% EQU 0 (
    echo Python version is compatible with Coqui TTS. Installing...
    pip install git+https://github.com/coqui-ai/TTS.git
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install Coqui TTS. The library will run in simulation mode.
    )
) else (
    echo Python version is not compatible with Coqui TTS (requires 3.9-3.11).
    echo AutoTune will run in simulation mode without actual TTS functionality.
    echo To use full functionality, create a virtual environment with Python 3.9-3.11.
)

echo.
echo Setup complete! Virtual environment is now active.
echo To deactivate the virtual environment, run: deactivate
echo.
echo To use AutoTune, you can:
echo 1. Run the example: python examples/basic_usage.py
echo 2. Use the CLI: python app/app.py --help
echo.