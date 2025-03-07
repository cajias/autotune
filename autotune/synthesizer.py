"""
Voice synthesis using trained models
"""
import os
import json
from pathlib import Path
from typing import Optional

import torch
import numpy as np
import soundfile as sf

# Import TTS conditionally to handle compatibility issues
try:
    from TTS.tts.configs.xtts_config import XttsConfig
    from TTS.tts.models.xtts import Xtts
    HAS_TTS = True
except ImportError:
    HAS_TTS = False
    print("Warning: Coqui TTS not available. Using simulated TTS functionality.")

from .voice_model import VoiceModel


class VoiceSynthesizer:
    """Synthesizes speech using trained voice models"""
    
    def __init__(self, use_gpu: bool = True):
        """
        Initialize the synthesizer
        
        Args:
            use_gpu: Whether to use GPU for inference if available
        """
        self.device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        self.current_model = None
        self.tts_model = None
        
        if not HAS_TTS:
            print("Running in simulation mode: TTS functionality will be simulated")
    
    def load_model(self, voice_model: VoiceModel) -> None:
        """
        Load a voice model for synthesis
        
        Args:
            voice_model: The voice model to load
        """
        print(f"Loading voice model: {voice_model.name}")
        
        self.current_model = voice_model
        
        if HAS_TTS:
            try:
                config = XttsConfig()
                config.load_json(voice_model.config_path)
                self.tts_model = Xtts.init_from_config(config)
                self.tts_model.load_checkpoint(config, voice_model.model_path)
                self.tts_model.to(self.device)
                print(f"Model '{voice_model.name}' loaded successfully")
            except Exception as e:
                print(f"Error loading TTS model: {e}")
                print("Falling back to simulation mode")
                self.tts_model = None
        else:
            print(f"Model '{voice_model.name}' loaded in simulation mode")
    
    def synthesize(self, 
                  text: str, 
                  output_path: Optional[str] = None,
                  speaker_wav: Optional[str] = None,
                  language: str = "en") -> str:
        """
        Synthesize speech from text
        
        Args:
            text: The text to synthesize
            output_path: Path to save the synthesized audio (optional)
            speaker_wav: Path to a reference audio file for speaker characteristics (optional)
            language: Language code for synthesis
            
        Returns:
            Path to the synthesized audio file
        """
        if self.current_model is None:
            raise ValueError("No voice model loaded. Call load_model() first.")
            
        print(f"Synthesizing: '{text}'")
        
        # Create output path if not provided
        if output_path is None:
            output_dir = Path("synthesized")
            output_dir.mkdir(exist_ok=True)
            output_path = str(output_dir / f"speech_{hash(text) % 10000}.wav")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if HAS_TTS and self.tts_model is not None:
            try:
                wav = self.tts_model.synthesize(
                    text=text,
                    speaker_wav=speaker_wav,
                    language=language
                )
                sf.write(output_path, wav, 22050)
                print(f"Speech synthesized and saved to: {output_path}")
            except Exception as e:
                print(f"Error during synthesis: {e}")
                print("Creating a dummy audio file instead")
                dummy_audio = np.zeros(22050)  # 1 second of silence
                sf.write(output_path, dummy_audio, 22050)
        else:
            # Simulation mode - create a dummy audio file
            print("Using simulation mode for synthesis")
            dummy_audio = np.zeros(22050)  # 1 second of silence
            sf.write(output_path, dummy_audio, 22050)
            print(f"Dummy audio saved to: {output_path}")
        
        return output_path