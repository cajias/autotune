```
   ___       _      _____
  / _ \     | |    |_   _|
 / /_\ \_   _| |_ ___ | |_   _ _ __   ___
 |  _  | | | | __/ _ \| | | | | '_ \ / _ \
 | | | | |_| | || (_) | | |_| | | | |  __/
 \_| |_/\__,_|\__\___/\_/\__,_|_| |_|\___|
```

<p align="center">
  <strong>Clone a voice and turn text into speech &mdash; a small Python toolkit built on Coqui&nbsp;TTS.</strong>
</p>

<p align="center">
  <a href="https://github.com/cajias/autotune/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/cajias/autotune"></a>
  <img alt="Top language" src="https://img.shields.io/github/languages/top/cajias/autotune">
  <img alt="Last commit" src="https://img.shields.io/github/last-commit/cajias/autotune">
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%E2%80%933.11-blue?logo=python&logoColor=white">
  <img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white">
  <img alt="Coqui TTS" src="https://img.shields.io/badge/Coqui-TTS-22a699">
</p>

---

AutoTune is a voice-cloning and text-to-speech toolkit that wraps [Coqui TTS](https://github.com/coqui-ai/TTS) behind a friendly Python API and CLI. Record a handful of voice samples with the built-in teleprompter, train a model, and synthesize speech in your own voice &mdash; or pull a pre-trained model and start generating audio right away. When Coqui TTS is not installed, AutoTune runs in **simulation mode** so you can exercise the full workflow without the heavy dependency.

## ✨ Features

- **Interactive recording studio** &mdash; a `curses` teleprompter (`scripts/record_session.py`) walks you through ten scripted, one-minute takes and tracks your progress across sessions.
- **Voice model training** &mdash; turn your recordings into a named voice model via the `VoiceTrainer` API or the `train` CLI command.
- **Speech synthesis** &mdash; generate WAV output from any text with the `VoiceSynthesizer` API or the `speak` CLI command, with optional speaker-reference audio and language selection.
- **Pre-trained model support** &mdash; list and download Coqui TTS models with `scripts/download_models.py`.
- **Simulation mode** &mdash; the library degrades gracefully when Coqui TTS is unavailable, so the API and CLI stay importable and testable.
- **Cross-platform setup scripts** &mdash; one-shot environment bootstrap for both `setup_venv.sh` and `setup_venv.bat`.

## 📦 Installation

AutoTune targets **Python 3.9&ndash;3.11** (3.11 recommended; Coqui TTS does not support 3.12+).

```bash
git clone https://github.com/cajias/autotune.git
cd autotune

# Create and populate a virtual environment, install AutoTune (-e),
# and attempt to install Coqui TTS if your Python version supports it.
./setup_venv.sh        # Windows: setup_venv.bat
```

Prefer to do it by hand?

```bash
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
pip install git+https://github.com/coqui-ai/TTS.git   # optional: real TTS
```

Without the Coqui TTS step the package still installs and runs, but in simulation mode.

## 🚀 Usage

### Command-line interface

The primary CLI lives in `app/app.py` and exposes three subcommands:

```bash
# Train a voice model from audio files or directories of .wav files
python app/app.py train my_voice --audio recordings/my_voice --epochs 1000 --batch-size 16

# List the voice models you have trained
python app/app.py list

# Synthesize speech with a trained model
python app/app.py speak my_voice --text "Hello from my cloned voice." --output out.wav
```

By default models are stored under `~/.autotune/models`; override this with the global `--models-dir` flag. The `speak` command also accepts `--text-file`, `--speaker-wav`, `--language` (default `en`), and `--cpu` to force CPU inference.

### Recording, training, and synthesizing with the scripts

```bash
# 1. Record voice samples with the teleprompter (add --simple for a plain prompt)
python scripts/record_session.py your_name

# 2. Train a model from the recorded sessions
python scripts/train_voice.py your_name --epochs 1000

# 3. Browse and fetch pre-trained Coqui models
python scripts/download_models.py --list
python scripts/download_models.py --download tts_models/en/ljspeech/vits

# 4. Synthesize from a model
python examples/synthesize.py --model vits --text "Hello, this is a test."
```

### Python API

```python
from autotune import VoiceTrainer, VoiceSynthesizer

trainer = VoiceTrainer(models_dir="models")
model = trainer.create_voice_model("my_voice")
trainer.train(model, ["sample1.wav", "sample2.wav"], epochs=1000)

synth = VoiceSynthesizer(use_gpu=True)
synth.load_model(model)
synth.synthesize(text="Hello, world!", output_path="output/hello.wav")
```

See `examples/basic_usage.py` for an end-to-end walkthrough.

## 🗂️ Project Structure

```
autotune/
├── app/
│   └── app.py              # Primary CLI: train / list / speak subcommands
├── autotune/               # Core library package
│   ├── __init__.py         # Public API + simulation-mode detection
│   ├── voice_model.py      # VoiceModel: model files & metadata management
│   ├── trainer.py          # VoiceTrainer: build and train voice models
│   └── synthesizer.py      # VoiceSynthesizer: text-to-speech inference
├── examples/
│   ├── basic_usage.py      # End-to-end library demo
│   └── synthesize.py       # Synthesize speech from a saved model
├── scripts/
│   ├── record_session.py   # Interactive teleprompter recorder
│   ├── train_voice.py      # Train from recorded sessions
│   ├── download_models.py  # List/download pre-trained Coqui models
│   └── requirements.txt    # Extra deps for the recording scripts
├── requirements.txt        # Runtime dependencies
├── setup.py                # Package configuration
├── setup_venv.sh           # Environment bootstrap (Unix)
├── setup_venv.bat          # Environment bootstrap (Windows)
└── mise.toml               # Pins Python 3.11 via mise
```

## 🛠️ Development

```bash
# Set up the environment in editable mode
./setup_venv.sh

# Verify the package imports (requires torch installed)
python -c "import autotune; print(autotune.__version__)"

# Run the end-to-end example (works in simulation mode)
python examples/basic_usage.py

# Inspect the CLI surface
python app/app.py --help
```

> The library imports `torch` at load time, so an environment with PyTorch installed is required to import the package or run the CLI. There is currently no automated test suite.

## 🤝 Contributing

Contributions are welcome. Fork the repository, create a feature branch, keep changes focused, and open a pull request describing what changed and why. Please match the existing code style and update the README when behavior changes.

## 📄 License

Released under the [MIT License](LICENSE). Copyright © 2026 Raul Cajias.
