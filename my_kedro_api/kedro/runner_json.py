# File: your_app/kedro/runner.py
from kedro.runner import SequentialRunner
from kedro.io import DataCatalog, MemoryDataset
from kedro_datasets.json import JSONDataset  # there are many other dataset types, e.g. CSV, Parquet, etc. https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-5.1.0/
from .pipeline import create_pipeline
import os
from pathlib import Path
from datetime import datetime

def ensure_data_dir():
    """Ensure the data directory exists."""
    data_dir = Path("data/processed")
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def run_pipeline_json(input_data: dict) -> dict:
    """
    The interface that expose to django ninja API directly:
    1. Create pipeline instance
    2. Run the Kedro pipeline and save to JSON
    """
    # Ensure data directory exists
    data_dir = ensure_data_dir()
    
    # Create a unique filename using timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = data_dir / f"processed_data_{timestamp}.json"
    
    # Configure data catalog with JSON output, basically define the input, output data source and format
    data_catalog = DataCatalog({
        "input_data": MemoryDataset(input_data),
        "processed_data": JSONDataset(
            filepath=str(json_path),
            save_args={
                "indent": 2  # Pretty print JSON
            }
        )
    })
    
    # Create and run pipeline
    pipeline = create_pipeline()
    SequentialRunner().run(pipeline, data_catalog)  # ! this will issue a lot side tasks: data catalog save, load, etc.
    
    # Load and return the processed data
    return data_catalog.load("processed_data")

# Optional: File management utilities
def cleanup_old_files(max_files: int = 100):
    """Keep only the most recent N files."""
    data_dir = Path("data/processed")
    files = sorted(data_dir.glob("*.json"), key=os.path.getmtime, reverse=True)
    for file in files[max_files:]:
        file.unlink()

def get_latest_processed_file() -> Path:
    """Get the most recent processed file."""
    data_dir = Path("data/processed")
    files = sorted(data_dir.glob("*.json"), key=os.path.getmtime, reverse=True)
    return files[0] if files else None