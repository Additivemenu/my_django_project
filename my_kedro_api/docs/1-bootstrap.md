simple setup for kedro pipeline 


# how to setup simple kedro pipeline within django?

+ absolutely no need to bootstrap using kedro command!
  + just with kedro and kedro-dataset installed
  + chat link: https://claude.ai/chat/824c10dd-333d-48b1-867c-3b17f19e65f4

I'll show you how to add Kedro to your existing Django app by creating the necessary files.



```python
# First, install required packages with Poetry:
# poetry add kedro django-ninja pandas

# File: your_app/kedro/nodes.py
import pandas as pd

def process_data(data: dict) -> dict:
    """Process input data and return results."""
    df = pd.DataFrame([data])
    # Example processing: multiply numeric values by 2
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    df[numeric_columns] = df[numeric_columns] * 2
    return df.to_dict(orient='records')[0]

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

# File: your_app/kedro/runner.py
from kedro.runner import SequentialRunner
from kedro.io import DataCatalog, MemoryDataset
from .pipeline import create_pipeline

def run_pipeline(input_data: dict) -> dict:
    """Run the Kedro pipeline with the given input data."""
    data_catalog = DataCatalog({
        "input_data": MemoryDataSet(input_data),
        "processed_data": MemoryDataSet()
    })
    
    pipeline = create_pipeline()
    SequentialRunner().run(pipeline, data_catalog)
    
    return data_catalog.load("processed_data")

# File: your_app/api.py
from ninja import NinjaAPI, Schema
from typing import Dict, Any
from .kedro.runner import run_pipeline

api = NinjaAPI()

class InputData(Schema):
    data: Dict[str, Any]

class OutputData(Schema):
    result: Dict[str, Any]

@api.post("/process", response=OutputData)
def process_data(request, input_data: InputData):
    """Process data through the Kedro pipeline."""
    result = run_pipeline(input_data.data)
    return {"result": result}

# File: your_app/urls.py
# Add this to your existing urls.py
from django.urls import path
from .api import api

urlpatterns = [
    # ... your existing URLs
    path("api/", api.urls),
]

```

To integrate this into your existing Django app:

1. First, install the required packages:
```bash
poetry add kedro django-ninja pandas
```

2. Create a `kedro` directory in your existing app:
```bash
mkdir your_app/kedro
touch your_app/kedro/__init__.py
```

3. Copy each file from above into the corresponding location in your app structure:
```
your_app/
├── kedro/
│   ├── __init__.py
│   ├── nodes.py
│   ├── pipeline.py
│   └── runner.py
├── api.py
└── urls.py  # Update your existing urls.py
```

4. Make sure your app's URLs are included in your project's main `urls.py`.

You can then test the pipeline by sending a POST request:
```bash
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{"data": {"value": 10, "text": "test"}}'
```

This gives you a minimal Kedro setup with:
- A single node pipeline that can process data
- A Django Ninja API endpoint to trigger it
- Memory-based data storage

You can modify the `process_data` function in `nodes.py` to implement your actual data processing logic.

Would you like me to explain any part in more detail or help you customize the pipeline for your specific needs?