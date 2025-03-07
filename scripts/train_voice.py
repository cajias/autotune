#!/usr/bin/env python
"""
Train a voice model using recorded samples
"""
import os
import json
import argparse
from pathlib import Path

from autotune import VoiceModel, VoiceTrainer

def collect_recordings(user_id):
    """Collect all recordings for a user"""
    recordings_dir = Path("recordings") / user_id
    
    if not recordings_dir.exists():
        raise ValueError(f"No recordings found for user {user_id}")
    
    # Check session info
    info_file = recordings_dir / "session_info.json"
    if not info_file.exists():
        raise ValueError(f"No session information found for user {user_id}")
    
    with open(info_file, 'r') as f:
        info = json.load(f)
    
    # Collect all WAV files from completed sessions
    audio_files = []
    for session_num in info["completed_sessions"]:
        session_dir = recordings_dir / f"session_{session_num}"
        recording = session_dir / f"recording_{session_num}.wav"
        if recording.exists():
            audio_files.append(str(recording))
    
    return audio_files, info

def main():
    parser = argparse.ArgumentParser(description="Train a voice model from recorded samples")
    parser.add_argument("user_id", help="Unique identifier for the user")
    parser.add_argument("--model-name", help="Name for the trained model (default: user_id)")
    parser.add_argument("--epochs", type=int, default=1000, help="Number of training epochs")
    args = parser.parse_args()
    
    # Use user_id as model name if not specified
    model_name = args.model_name or args.user_id
    
    try:
        # Collect recordings
        print(f"Collecting recordings for user {args.user_id}...")
        audio_files, info = collect_recordings(args.user_id)
        
        if not audio_files:
            print("No recordings found!")
            return
        
        print(f"Found {len(audio_files)} recordings")
        
        # Initialize trainer
        trainer = VoiceTrainer()
        
        # Create and train model
        print(f"\nCreating voice model: {model_name}")
        model = trainer.create_voice_model(model_name)
        
        print("\nTraining model...")
        print("This may take a while depending on the amount of data and training parameters")
        
        trained_model = trainer.train(
            model,
            audio_files,
            epochs=args.epochs
        )
        
        print(f"\nModel training completed!")
        print(f"Model saved to: {trained_model.model_path}")
        print("\nYou can now use this model with the synthesize.py script:")
        print(f"python examples/synthesize.py --model {model_name}")
        
    except Exception as e:
        print(f"Error during training: {e}")

if __name__ == "__main__":
    main()