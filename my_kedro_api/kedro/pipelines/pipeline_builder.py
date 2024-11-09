from kedro.pipeline import Pipeline, node
import pandas as pd
from typing import List, Callable, Dict, Any
from .nodes.enhance_num import enhance_num
from .nodes.transform_text import transform_text

class PipelineBuilder:
    """Builds Kedro pipelines dynamically."""
    
    def __init__(self):
        # Register available nodes with their names
        self.available_nodes: Dict[str, Callable] = {
            "enhance_numbers": enhance_num,
            "transform_text": transform_text
        }
        self.node_sequence: List[str] = []  # will use this to build the pipeline, just a blue print
        
    def add_node(self, node_name: str) -> 'PipelineBuilder':
        """Add a node to the pipeline sequence."""
        if node_name not in self.available_nodes:
            raise ValueError(f"Node {node_name} not found. Available nodes: {list(self.available_nodes.keys())}")
        
        self.node_sequence.append(node_name)
        return self
    
    def build(self) -> Pipeline:
        """Build the pipeline based on the specified sequence."""
        if not self.node_sequence:
            raise ValueError("No nodes added to pipeline")
        
        pipeline_nodes = []
        
        # Create first node
        first_node = node(
            func=self.available_nodes[self.node_sequence[0]],
            inputs="input_data",
            outputs=f"data_{0}",
            name=f"node_{self.node_sequence[0]}"
        )
        pipeline_nodes.append(first_node)
        
        # Create subsequent nodes
        for idx, node_name in enumerate(self.node_sequence[1:], 1):
            current_node = node(
                func=self.available_nodes[node_name],
                inputs=f"data_{idx-1}",
                outputs=f"data_{idx}" if idx < len(self.node_sequence)-1 else "output_data",
                name=f"node_{node_name}"
            )
            pipeline_nodes.append(current_node)
        
        return Pipeline(pipeline_nodes)

# Usage example:
"""
# Build pipeline that enhances numbers then transforms text
builder = PipelineBuilder()
pipeline = (builder
    .add_node("enhance_numbers")
    .add_node("transform_text")
    .build())

# Build pipeline that only transforms text
text_only_pipeline = (PipelineBuilder()
    .add_node("transform_text")
    .build())
"""