import pandas as pd
from io import BytesIO

def process_file(content: bytes, filename: str) -> pd.DataFrame:
    """Read file bytes into a pandas DataFrame."""
    try:
        filename_lower = filename.lower()
        if filename_lower.endswith('.csv'):
            return pd.read_csv(BytesIO(content))
        elif filename_lower.endswith(('.xls', '.xlsx')):
            return pd.read_excel(BytesIO(content))
        else:
            raise ValueError("Unsupported file format. Please upload CSV or Excel.")
    except Exception as e:
        raise ValueError(f"Failed to process file: {str(e)}")

