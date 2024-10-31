# File: your_app/kedro/datasets/custom_json_dataset.py
from kedro.io import AbstractDataset
from pathlib import Path
import json
from typing import Any, Dict
from datetime import datetime


class CustomJsonDataset(AbstractDataset):
    """
    Custom dataset that handles JSON with additional metadata, dataset will be saved to local json file at certain path.
    
    kedro provides very powerful and flexible data catalog and dataset system. 
    
    """
    def __init__(
        self,
        filepath: str,
        version: str = None,
        save_args: Dict[str, Any] = None,
    ):
        # Fix: Simply convert filepath to Path directly
        self._filepath = Path(filepath)
        self._save_args = save_args or {"indent": 2}

    def _load(self) -> Dict[str, Any]:
        """Loads data from the JSON file."""
        if not self._filepath.exists():
            raise FileNotFoundError(f"File not found: {self._filepath}")
            
        with self._filepath.open("r") as f:
            data = json.load(f)
            
        # Add custom validation
        required_fields = ["processed_at", "data"]
        if not all(field in data for field in required_fields):
            raise ValueError(f"JSON must contain fields: {required_fields}")
            
        return data

    def _save(self, data: Dict[str, Any]) -> None:
        """
        Saves data to the JSON file with metadata.
        """
        # Add metadata
        enhanced_data = {
            "data": data,
            "processed_at": datetime.now().isoformat(),
            "version": "1.0",
            "metadata": {
                "source": "kedro_pipeline",
                "created_at": datetime.now().isoformat()
            }
        }
        
        self._filepath.parent.mkdir(parents=True, exist_ok=True)
        with self._filepath.open("w") as f:
            json.dump(enhanced_data, f, **self._save_args)

    def _describe(self) -> Dict[str, Any]:
        """
        Returns a description of the dataset.
        """
        return {
            "filepath": str(self._filepath),
            "save_args": self._save_args
        }