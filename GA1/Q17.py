import os, json, re, pytz, subprocess
import zipfile
import shutil
import tempfile
import hashlib
from datetime import datetime

def execute(question: str, parameter, file_bytes: None):
    return compare_files(parameter["_file_"])

def compare_files(file):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Save uploaded ZIP file
        zip_path = os.path.join(temp_dir, file.filename)
        with open(zip_path, "wb") as buffer:
            file.file.seek(0)
            shutil.copyfileobj(file.file, buffer)

        # Extract ZIP file
        extracted_dir = os.path.join(temp_dir, "extracted")
        os.makedirs(extracted_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extracted_dir)
        
        # Step 2: Read both files
        a_path = os.path.join(extracted_dir, "a.txt")
        b_path = os.path.join(extracted_dir, "b.txt")

        with open(a_path, 'r', encoding='utf-8') as f1, open(b_path, 'r', encoding='utf-8') as f2:
            a_lines = f1.readlines()
            b_lines = f2.readlines()

        # Step 3: Count differing lines
        differing_lines = sum(1 for a, b in zip(a_lines, b_lines) if a != b)
        print("🔍 Number of differing lines:", differing_lines)
        return differing_lines
        
    except Exception as e:
        return {"error": str(e)}

    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)