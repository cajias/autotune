"""
Voice model representation and management
"""
import os
import json
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class VoiceModel:
    """Represents a trained voice model"""
    
    def __init__(self, name: str, model_path: str, config_path: str, metadata_path: str):
        """
        Initialize a voice model
        
        Args:
            name: Name of the voice model
            model_path: Path to the model file
            config_path: Path to the model configuration file
            metadata_path: Path to the model metadata file
        """
        self.name = name
        self.model_path = model_path
        self.config_path = config_path
        self.metadata_path = metadata_path
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load metadata from file or create default metadata"""
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading metadata: {e}")
                return self._create_default_metadata()
        else:
            return self._create_default_metadata()
    
    def _create_default_metadata(self) -> Dict[str, Any]:
        """Create default metadata for a new model"""
        return {
            "name": self.name,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "samples_used": 0,
            "training_duration": 0,
            "description": "",
            "language": "en"
        }
    
    def update_metadata(self, **kwargs) -> None:
        """Update model metadata with new values"""
        self.metadata.update(kwargs)
        self.metadata["updated_at"] = datetime.now().isoformat()
        
        with open(self.metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def get_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "name": self.name,
            "created_at": self.metadata.get("created_at", "Unknown"),
            "updated_at": self.metadata.get("updated_at", "Unknown"),
            "samples_used": self.metadata.get("samples_used", 0),
            "training_duration": self.metadata.get("training_duration", 0),
            "description": self.metadata.get("description", ""),
            "language": self.metadata.get("language", "en"),
            "model_path": self.model_path,
            "config_path": self.config_path
        }
    
    @classmethod
    def create(cls, name: str, models_dir: str) -> 'VoiceModel':
        """
        Create a new voice model
        
        Args:
            name: Name of the voice model
            models_dir: Directory to store models
            
        Returns:
            A new VoiceModel instance
        """
        model_dir = Path(models_dir) / name
        model_dir.mkdir(parents=True, exist_ok=True)
        
        model_path = str(model_dir / "model.pth")
        config_path = str(model_dir / "config.json")
        metadata_path = str(model_dir / "metadata.json")
        
        return cls(name, model_path, config_path, metadata_path)
    
    @classmethod
    def load(cls, model_dir: Path) -> 'VoiceModel':
        """
        Load a voice model from a directory
        
        Args:
            model_dir: Directory containing the model files
            
        Returns:
            A VoiceModel instance
        """
        name = model_dir.name
        
        # Handle both cases: model file directly in model_dir or in a subdirectory
        model_path = model_dir / "model.pth"
        if not model_path.exists():
            # Look for model files in subdirectories
            model_files = list(model_dir.glob("**/model.pth"))
            if model_files:
                model_path = model_files[0]
        
        # Handle both cases: config file directly in model_dir or in a subdirectory
        config_path = model_dir / "config.json"
        if not config_path.exists():
            # Look for config files in subdirectories
            config_files = list(model_dir.glob("**/config.json"))
            if config_files:
                config_path = config_files[0]
        
        metadata_path = model_dir / "metadata.json"
        
        return cls(name, str(model_path), str(config_path), str(metadata_path))