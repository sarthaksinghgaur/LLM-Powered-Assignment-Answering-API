import os, json, io, pandas as pd, zipfile, re
from bs4 import BeautifulSoup

def execute(question: str, parameter, file_bytes=None):
    file = io.BytesIO(file_bytes) if file_bytes else None
    sum = process_unicode_data(file, question)
    return sum

def process_unicode_data(zip_file, question):
    
    # Step 1: Extract substring between "symbol matches" and "across"
    match = re.search(r"symbol matches (.+?) across", question)
    if match:
        symbol_text = match.group(1)  # Extracted text between the keywords
        symbols = [sym.strip() for sym in symbol_text.split(" OR ")]  # Split by ' OR ' and clean spaces
    else:
        raise ValueError("No symbols found in the sentence.")

    
    target_symbols = symbols[-3:]
    
    # Process each file with correct encoding and delimiter
    files = [
        ("data1.csv", "cp1252", ","),
        ("data2.csv", "utf-8", ","),
        ("data3.txt", "utf-16", "\t"),
    ]
    symbols_count = 0  # Initialize delimiter counter
    total = 0
    # Extract the zip file
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for filename, encoding, delimiter in files:
            with zip_ref.open(filename) as txt_file:
                data = txt_file.read().decode(encoding)  # Decode using correct encoding
                # Loop through lines and count delimiter occurrences
                for line in data.splitlines():
                    for symbol in target_symbols:
                        if symbol in line:
                            line_split = line.split(delimiter)
                            if len(line_split) > 1:
                                amount = int(line_split[1])
                                total += amount
                            else:
                                raise ValueError("No amount found in the line.")
    return total