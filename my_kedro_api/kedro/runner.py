# File: your_app/kedro/runner.py
from kedro.runner import SequentialRunner
from kedro.io import DataCatalog, MemoryDataset
from .pipeline import create_pipeline

def run_pipeline(input_data: dict) -> dict:
    """
    The interface that expose to django ninja API directly:
        1. Create pipeline instance (here is just a static pipeline, we can wrap this runner with a KedroManager to allow user create and run dynamic pipeline).
        2. Run the Kedro pipeline with the given input data.
    """
    
    # step1: link data catalog
    # it may also comes from local storage or even remote storage, e.g. S3, GCS, etc.
    data_catalog = DataCatalog({
        "input_data": MemoryDataset(input_data),
        "processed_data": MemoryDataset()
    })
    
    # step2: create pipeline
    # like have a pipeline builder class to create pipeline instance dynamically
    pipeline = create_pipeline()
    
    # step3: run pipeline
    # you can also choose to use other runner, e.g. ParallelRunner
    SequentialRunner().run(pipeline, data_catalog)
    
    return data_catalog.load("processed_data")