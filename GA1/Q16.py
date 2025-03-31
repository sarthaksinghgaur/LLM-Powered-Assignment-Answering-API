import os, json, re, pytz, subprocess
import zipfile
import shutil
import tempfile
import hashlib
from datetime import datetime

def execute(question: str, parameter, file_bytes: None):
    return move_and_rename_files(parameter["_file_"])
        
def move_and_rename_files(file):
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
        expected_dir = os.path.join(temp_dir, "expected")
        os.makedirs(extracted_dir, exist_ok=True)
        os.makedirs(expected_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extracted_dir)
        
        # 2. Move all files from subfolders into base_dir
        for root, _, files in os.walk(extracted_dir):
            for file in files:
                src = os.path.join(root, file)
                new_name = rename_digits(file)
                dst = os.path.join(expected_dir, new_name)
                shutil.move(src, dst)

        # 3. Run: grep . * | LC_ALL=C sort | sha256sum
        result = subprocess.check_output(
            "grep . * | LC_ALL=C sort | sha256sum",
            shell=True,
            cwd=expected_dir
        ).decode().strip()

        print("✅ Final SHA-256 Output:\n", result)
        return result
        
    except Exception as e:
        return {"error": str(e)}

    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)
        
def transform_digit(c):
    return str((int(c) + 1) % 10)

def rename_digits(name):
    return ''.join(transform_digit(c) if c.isdigit() else c for c in name)