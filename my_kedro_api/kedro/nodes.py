# File: your_app/kedro/nodes.py
import pandas as pd

def process_data(data: dict) -> dict:
    """Process input data and return results."""
    df = pd.DataFrame([data])
    
    # Example processing: multiply numeric values by 2
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    df[numeric_columns] = df[numeric_columns] * 2
    return df.to_dict(orient='records')[0]