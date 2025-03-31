import os, json, pandas as pd, io, re

def execute(question: str, parameter, file_bytes = None):
        total_sales_value = total_sales(parameter["_file_"])
        return total_sales_value
        
def total_sales(fileObj, sales_key="sales"):
    fileObj.file.seek(0)
    """
    Calculates the total sales from a JSONL file with potentially malformed data.

    Parameters:
    - file_path (str): Path to the JSONL file.
    - sales_key (str): The key used to extract sales values from JSON objects.

    Returns:
    - int: The total sum of sales values.
    """
    total_sales = 0

    def extract_sales_from_line(line):
        """Attempt to manually extract sales value from a malformed line."""
        match = re.search(rf'"{sales_key}":\s*(\d+)', line)
        return int(match.group(1)) if match else 0

    #with open(fileObj, "r", encoding="utf-8") as file:
    #fileObj = fileObj.read()
    for line in fileObj.file:
        line = str(line).strip()  # Remove leading/trailing whitespace
        try:
            # Try to decode the JSON line
            data = json.loads(line)
            total_sales += data.get(sales_key, 0)
        except json.JSONDecodeError:
            # If decoding fails, extract sales manually from the corrupted line
            sales_value = extract_sales_from_line(line)
            total_sales += sales_value
            #print(f"Corrupted line, sales extracted: {sales_value}")

    return total_sales
        
        