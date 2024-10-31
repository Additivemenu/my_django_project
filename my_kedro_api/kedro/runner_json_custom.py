# File: your_app/kedro/runner_json_custom.py
from pathlib import Path
from datetime import datetime

from kedro.runner import SequentialRunner
from kedro.io import DataCatalog, MemoryDataset
from .pipeline import create_pipeline
from .datasets.custom_json_dataset import CustomJsonDataset


def ensure_data_dir():
    """Ensure the data directory exists."""
    data_dir = Path("data/processed")
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def run_pipeline_json_custom(input_data: dict) -> dict:
    """Run pipeline with custom dataset."""
    data_dir = ensure_data_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = data_dir / f"processed_data_{timestamp}.json"
    
    # Configure data catalog with custom dataset
    data_catalog = DataCatalog({
        "input_data": MemoryDataset(input_data),
        
        # ! note here we used custom dataset
        "processed_data": CustomJsonDataset(
            filepath=str(json_path),  # Convert Path to string
            save_args={
                "indent": 2,
                "ensure_ascii": False
            }
        )
    })
    
    pipeline = create_pipeline()
    SequentialRunner().run(pipeline, data_catalog)
    
    
    
    # Load and return just the data portion
    result = data_catalog.load("processed_data")  # this will read the file defined by CustomJsonDataset
    
    return result["data"]  # Return only the actual data, not the metadata