# File: your_app/kedro/pipeline.py
from kedro.pipeline import Pipeline, node
from .nodes import process_data

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=process_data,
                inputs="input_data",
                outputs="processed_data",
                name="process_data_node",
            ),
        ]
    )
