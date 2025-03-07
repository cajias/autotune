#!/usr/bin/env python
"""
Script to download pre-trained TTS models from Coqui TTS
"""
import os
import sys
import argparse
from pathlib import Path

try:
    from TTS.utils.manage import ModelManager
    from TTS.utils.synthesizer import Synthesizer
    HAS_TTS = True
except ImportError:
    HAS_TTS = False
    print("Error: Coqui TTS is not installed. Please install it first.")
    print("pip install TTS")
    sys.exit(1)

def download_model(model_name, output_dir):
    """Download a pre-trained model from Coqui TTS"""
    print(f"Downloading model: {model_name}")
    
    # Initialize model manager
    model_manager = ModelManager(output_path=output_dir)
    
    # Download the model
    try:
        model_path, config_path = model_manager.download_model(model_name)
        print(f"Model downloaded successfully to: {model_path}")
        print(f"Config file: {config_path}")
        return True
    except Exception as e:
        print(f"Error downloading model: {e}")
        return False

def list_available_models():
    """List all available pre-trained models"""
    print("Available pre-trained models:")
    
    # Initialize model manager
    model_manager = ModelManager()
    
    # Get available models
    model_names = model_manager.list_models()
    
    # Print models
    print("\n Name format: type/language/dataset/model")
    for i, model_name in enumerate(model_names, 1):
        print(f" {i}: {model_name}")

def setup_model_directory(model_name, output_dir):
    """Set up a directory structure for a voice model"""
    # Extract the model name from the full path
    model_short_name = model_name.split('/')[-1]
    
    model_dir = Path(output_dir) / model_short_name
    model_dir.mkdir(parents=True, exist_ok=True)
    
    return model_dir

def main():
    parser = argparse.ArgumentParser(description="Download pre-trained TTS models")
    parser.add_argument("--list", action="store_true", help="List available models")
    parser.add_argument("--download", type=str, help="Download a specific model")
    parser.add_argument("--output-dir", type=str, default="models", help="Output directory for downloaded models")
    
    args = parser.parse_args()
    
    if args.list:
        list_available_models()
        return
    
    if args.download:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up model directory
        model_dir = setup_model_directory(args.download, output_dir)
        
        # Download the model
        success = download_model(args.download, str(model_dir))
        
        if success:
            # Extract the model name from the full path
            model_short_name = args.download.split('/')[-1]
            
            print(f"\nModel '{model_short_name}' is ready to use.")
            print(f"You can use it with the following command:")
            print(f"python examples/synthesize.py --model {model_short_name}")
        return
    
    # If no arguments provided, show help
    parser.print_help()

if __name__ == "__main__":
    main()