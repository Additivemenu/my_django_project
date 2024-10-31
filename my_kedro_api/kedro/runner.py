# File: your_app/kedro/runner.py
from kedro.runner import SequentialRunner
from kedro.io import DataCatalog, MemoryDataSet
from .pipeline import create_pipeline
from pandas import MemoryDataset

def run_pipeline(input_data: dict) -> dict:
    """Run the Kedro pipeline with the given input data."""
    data_catalog = DataCatalog({
        "input_data": MemoryDataSet(input_data),
        "processed_data": MemoryDataSet()
    })
    
    pipeline = create_pipeline()
    SequentialRunner().run(pipeline, data_catalog)
    
    return data_catalog.load("processed_data")