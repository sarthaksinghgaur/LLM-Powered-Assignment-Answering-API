import zipfile
import pandas as pd
import io
import numpy as np

def execute(question: str, parameter, file_bytes):
    
    answer_values = get_column_from_zip(parameter["cvs_column_name"], file_bytes)
    return answer_values

def get_column_from_zip(column_name, file_bytes):
    try:
        with zipfile.ZipFile(io.BytesIO(file_bytes), 'r') as zip_ref:
            # Find the CSV file
            csv_files = [f for f in zip_ref.namelist() if f.lower().endswith('.csv')]

            if not csv_files:
                raise ValueError("No CSV file found in zip")

            # Read the CSV
            with zip_ref.open(csv_files[0]) as csv_file:
                df = pd.read_csv(csv_file)

    except Exception as e:
        raise ValueError(f"Error processing zip file: {str(e)}")

    # Step 3: Return the specified column
    if column_name not in df.columns:
        available = ", ".join(df.columns)
        raise ValueError(f"Column '{column_name}' not found. Available columns: {available}")

    return df[column_name].tolist() if len(df) > 1 else df[column_name].tolist()[0]