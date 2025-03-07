#!/usr/bin/env python3
"""
AutoTune CLI Application
A command-line tool for voice cloning and text-to-speech synthesis
"""
import os
import sys
import argparse
from pathlib import Path
from typing import List, Optional

# Add the parent directory to the path so we can import the autotune package
sys.path.insert(0, str(Path(__file__).parent.parent))

from autotune import VoiceModel, VoiceTrainer, VoiceSynthesizer


def train_command(args):
    """Handle the train command"""
    print(f"Training new voice model: {args.name}")
    
    # Check if audio files exist
    audio_files = []
    for pattern in args.audio:
        if os.path.isdir(pattern):
            # If directory, add all wav files
            for file in Path(pattern).glob("**/*.wav"):
                audio_files.append(str(file))
        elif os.path.isfile(pattern):
            # If file, add it directly
            audio_files.append(pattern)
        else:
            # Try glob pattern
            from glob import glob
            matches = glob(pattern)
            audio_files.extend(matches)
    
    if not audio_files:
        print(f"Error: No audio files found matching: {args.audio}")
        return 1
    
    print(f"Found {len(audio_files)} audio files for training")
    
    # Initialize trainer
    trainer = VoiceTrainer(models_dir=args.models_dir)
    
    # Create and train the model
    model = trainer.create_voice_model(args.name)
    trainer.train(
        model, 
        audio_files, 
        epochs=args.epochs,
        batch_size=args.batch_size
    )
    
    print(f"Model '{args.name}' trained successfully!")
    print(f"Model saved to: {Path(model.model_path).parent}")
    return 0


def list_command(args):
    """Handle the list command"""
    trainer = VoiceTrainer(models_dir=args.models_dir)
    models = trainer.list_models()
    
    if not models:
        print("No voice models found.")
        return 0
    
    print(f"Found {len(models)} voice models:")
    for model_name in models:
        try:
            model = trainer.get_model(model_name)
            created = model.metadata.get("created_at", "Unknown")
            samples = model.metadata.get("samples_used", "Unknown")
            print(f"  - {model_name} (Created: {created}, Samples: {samples})")
        except Exception as e:
            print(f"  - {model_name} (Error loading model: {e})")
    
    return 0


def speak_command(args):
    """Handle the speak command"""
    trainer = VoiceTrainer(models_dir=args.models_dir)
    
    try:
        model = trainer.get_model(args.model)
    except ValueError:
        print(f"Error: Model '{args.model}' not found")
        return 1
    
    # Get text from file or argument
    if args.text_file:
        with open(args.text_file, 'r') as f:
            text = f.read()
    else:
        text = args.text
    
    if not text:
        print("Error: No text provided for synthesis")
        return 1
    
    # Initialize synthesizer and generate speech
    synthesizer = VoiceSynthesizer(use_gpu=not args.cpu)
    synthesizer.load_model(model)
    
    output_path = synthesizer.synthesize(
        text=text,
        output_path=args.output,
        speaker_wav=args.speaker_wav,
        language=args.language
    )
    
    print(f"Speech synthesized and saved to: {output_path}")
    return 0


def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        description="AutoTune - Voice cloning and text-to-speech tool"
    )
    parser.add_argument(
        "--models-dir", 
        default=os.path.expanduser("~/.autotune/models"),
        help="Directory to store voice models"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Train command
    train_parser = subparsers.add_parser("train", help="Train a new voice model")
    train_parser.add_argument("name", help="Name for the new voice model")
    train_parser.add_argument(
        "--audio", 
        nargs="+", 
        required=True,
        help="Audio files or directories to use for training"
    )
    train_parser.add_argument(
        "--epochs", 
        type=int, 
        default=1000,
        help="Number of training epochs"
    )
    train_parser.add_argument(
        "--batch-size", 
        type=int, 
        default=16,
        help="Batch size for training"
    )
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available voice models")
    
    # Speak command
    speak_parser = subparsers.add_parser("speak", help="Synthesize speech with a voice model")
    speak_parser.add_argument("model", help="Name of the voice model to use")
    speak_parser.add_argument(
        "--text", 
        help="Text to synthesize"
    )
    speak_parser.add_argument(
        "--text-file", 
        help="File containing text to synthesize"
    )
    speak_parser.add_argument(
        "--output", 
        help="Output audio file path"
    )
    speak_parser.add_argument(
        "--speaker-wav", 
        help="Reference audio file for speaker characteristics"
    )
    speak_parser.add_argument(
        "--language", 
        default="en",
        help="Language code for synthesis (default: en)"
    )
    speak_parser.add_argument(
        "--cpu", 
        action="store_true",
        help="Force CPU inference even if GPU is available"
    )
    
    args = parser.parse_args()
    
    if args.command == "train":
        return train_command(args)
    elif args.command == "list":
        return list_command(args)
    elif args.command == "speak":
        return speak_command(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())