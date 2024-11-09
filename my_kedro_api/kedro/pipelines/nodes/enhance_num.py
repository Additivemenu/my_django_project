import pandas as pd

def enhance_num(data: dict) -> dict:
    """Process input data with enhanced output."""
    df = pd.DataFrame([data])
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    df[numeric_columns] = df[numeric_columns] * 2
    
    processed_data = df.to_dict(orient='records')[0]
    return processed_data