from ninja import Router, Schema
import pandas as pd
from typing import Dict, Any
from .kedro.runner import run_pipeline

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
    result = run_pipeline(input_data.data)
    return {"result": result}
