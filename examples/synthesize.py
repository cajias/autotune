#!/usr/bin/env python
"""
Example script to synthesize speech using a pre-trained model
"""
import os
import argparse
from pathlib import Path

from autotune import VoiceModel, VoiceSynthesizer

def main():
    parser = argparse.ArgumentParser(description="Synthesize speech using a pre-trained model")
    parser.add_argument("--model", type=str, required=True, help="Name of the model to use")
    parser.add_argument("--text", type=str, default="Hello, this is a test of the text to speech system.", 
                       help="Text to synthesize")
    parser.add_argument("--output", type=str, default="output/synthesized_speech.wav",
                       help="Output audio file path")
    parser.add_argument("--speaker", type=str, help="Path to speaker reference audio file (optional)")
    parser.add_argument("--language", type=str, default="en", help="Language code (default: en)")
    
    args = parser.parse_args()
    
    # Create output directory if needed
    output_dir = Path(args.output).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize synthesizer
    synthesizer = VoiceSynthesizer(use_gpu=True)
    
    # Load the model
    model = VoiceModel.load(Path("models") / args.model)
    synthesizer.load_model(model)
    
    # Synthesize speech
    output_path = synthesizer.synthesize(
        text=args.text,
        output_path=args.output,
        speaker_wav=args.speaker,
        language=args.language
    )
    
    print(f"\nSpeech synthesized and saved to: {output_path}")

if __name__ == "__main__":
    main()