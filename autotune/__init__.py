"""
AutoTune: A voice cloning and text-to-speech library using Coqui TTS
"""

from .voice_model import VoiceModel
from .trainer import VoiceTrainer
from .synthesizer import VoiceSynthesizer

__version__ = "0.1.0"

# Check if TTS is available
try:
    import TTS
    HAS_TTS = True
except ImportError:
    HAS_TTS = False
    print("Coqui TTS not available. AutoTune will run in simulation mode.")