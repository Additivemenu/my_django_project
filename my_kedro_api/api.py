from ninja import Router, Schema
import pandas as pd
from typing import Dict, Any
from .kedro.runner import run_pipeline
from .kedro.runner_json import run_pipeline_json
from .kedro.runner_json_custom import run_pipeline_json_custom

router = Router()

@router.get("/")
def index(request):
    return {"message": "Hello, world!"}

class InputData(Schema):
    data: Dict[str, Any]

class OutputData(Schema):
    result: Dict[str, Any]

@router.post("/process", response=OutputData)
def process_data(request, input_data: InputData):
    """Process data through the Kedro pipeline."""
    
    print("input data:", input_data)
    
    result = run_pipeline(input_data.data)
    return {"result": result}

@router.post("/process-json", response=OutputData)
def process_data_json(request, input_data: InputData):
    """Process data through the Kedro pipeline."""
    
    print("input data:", input_data)
    
    result = run_pipeline_json(input_data.data)
    return {"result": result}

@router.post("/process-json-custom", response=OutputData)
def process_data_json_custom(request, input_data: InputData):
    """Process data through the Kedro pipeline."""
    
    print("input data:", input_data)
    
    result = run_pipeline_json_custom(input_data.data)
    return {"result": result}