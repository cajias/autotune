# AutoTune

A voice cloning and text-to-speech library using Coqui TTS.

## Features

- Voice model training and synthesis
- Interactive recording tool with teleprompter interface
- Pre-trained model support
- Easy-to-use CLI tools

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd autotune
```

2. Create a virtual environment (Python 3.9-3.11 recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
./setup_venv.sh  # On Windows: setup_venv.bat
```

## Usage

### Recording Voice Samples

Use the interactive recording tool to create voice samples:

```bash
python scripts/record_session.py your_name
```

This will:
- Guide you through 10 recording sessions
- Show scrolling text to read
- Record 1-minute samples
- Track your progress

### Training a Voice Model

After recording samples, train your voice model:

```bash
python scripts/train_voice.py your_name
```

### Using Pre-trained Models

1. List available models:
```bash
python scripts/download_models.py --list
```

2. Download a model:
```bash
python scripts/download_models.py --download tts_models/en/ljspeech/vits
```

3. Synthesize speech:
```bash
python examples/synthesize.py --model vits --text "Hello, this is a test."
```

## Project Structure

```
autotune/
├── autotune/           # Main library code
│   ├── __init__.py
│   ├── synthesizer.py  # Voice synthesis
│   ├── trainer.py      # Model training
│   └── voice_model.py  # Model management
├── examples/           # Example scripts
│   ├── basic_usage.py
│   └── synthesize.py
├── scripts/            # Utility scripts
│   ├── download_models.py  # Download pre-trained models
│   ├── record_session.py   # Interactive recording tool
│   └── train_voice.py      # Train custom models
├── setup.py           # Package configuration
└── requirements.txt   # Dependencies
```

## Requirements

- Python 3.9-3.11 (3.11 recommended)
- PyTorch
- Coqui TTS
- sounddevice
- soundfile
- numpy

## License

MIT License