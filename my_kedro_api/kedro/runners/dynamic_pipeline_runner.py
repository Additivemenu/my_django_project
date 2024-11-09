from typing import List
from kedro.io import DataCatalog, MemoryDataset
from ..pipelines.pipeline_builder import PipelineBuilder
from kedro.runner import SequentialRunner

def run_dynamic_pipeline(input_data: dict, node_sequence: List[str]) -> dict:
    """Run a dynamically constructed pipeline."""
    # step1: bootstrap pipeline and data catalog
    # Create pipeline
    builder = PipelineBuilder()
    for node_name in node_sequence:
        builder.add_node(node_name)
    pipeline = builder.build()
    
    # Setup data catalog 
    # ! do we need catalog for each node?
    data_catalog = DataCatalog({
        "input_data": MemoryDataset(input_data)
    })
    # Add intermediate datasets
    for i in range(len(node_sequence)-1):
        data_catalog.add(f"data_{i}", MemoryDataset())
    # Add output dataset
    data_catalog.add("output_data", MemoryDataset())
    
    # step2: Run pipeline
    SequentialRunner().run(pipeline, data_catalog)  
    
    # step3: retrive output data from catalog
    return data_catalog.load("output_data")

# Example usage:
"""
input_data = {
    "name": "john",
    "value": 10
}
result = run_dynamic_pipeline(
    input_data,
    node_sequence=["enhance_numbers", "transform_text"]
)
"""