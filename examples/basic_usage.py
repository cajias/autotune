#!/usr/bin/env python3
"""
Basic usage example for the AutoTune library
"""
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the autotune package
sys.path.insert(0, str(Path(__file__).parent.parent))

from autotune import VoiceModel, VoiceTrainer, VoiceSynthesizer


def main():
    """Demonstrate basic usage of the AutoTune library"""
    # Set up directories
    models_dir = Path("./models")
    audio_dir = Path("./audio_samples")
    output_dir = Path("./output")
    
    models_dir.mkdir(exist_ok=True)
    audio_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    # Create a dummy audio file for demonstration
    if not list(audio_dir.glob("*.wav")):
        print("Creating a dummy audio file for demonstration...")
        import numpy as np
        import soundfile as sf
        
        # Create 3 seconds of silence as a placeholder
        dummy_audio = np.zeros(3 * 22050)
        sf.write(audio_dir / "sample.wav", dummy_audio, 22050)
    
    # Initialize the trainer
    trainer = VoiceTrainer(models_dir=str(models_dir))
    
    # Create and train a new voice model
    model_name = "example_voice"
    print(f"Creating and training voice model: {model_name}")
    
    model = trainer.create_voice_model(model_name)
    audio_files = [str(f) for f in audio_dir.glob("*.wav")]
    
    if not audio_files:
        print("Error: No audio files found in ./audio_samples")
        return 1
    
    trainer.train(model, audio_files, epochs=10, batch_size=8)
    
    # List available models
    print("\nAvailable voice models:")
    for model_name in trainer.list_models():
        print(f"  - {model_name}")
    
    # Load the model and synthesize speech
    print("\nSynthesizing speech with the trained model...")
    synthesizer = VoiceSynthesizer()
    synthesizer.load_model(model)
    
    text = "Hello, this is a demonstration of the AutoTune voice synthesis library."
    output_path = str(output_dir / "synthesized_speech.wav")
    
    synthesizer.synthesize(text=text, output_path=output_path)
    
    print(f"\nSpeech synthesized and saved to: {output_path}")
    print("Note: This is a simulated example. In a real implementation, actual voice synthesis would occur.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())