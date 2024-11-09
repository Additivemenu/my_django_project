import pandas as pd

def transform_text(data: dict) -> dict:
    """Transform text columns to uppercase."""
    df = pd.DataFrame([data])
    text_columns = df.select_dtypes(include=['object']).columns
    
    for col in text_columns:
        df[col] = df[col].str.upper()
    
    transformed_data = df.to_dict(orient='records')[0]
    return transformed_data