import os, json, re
import zipfile
import shutil
import tempfile
import hashlib

def execute(question: str, parameter, file_bytes):
    return upload_and_extract_zip(parameter["_file_"])
        
def upload_and_extract_zip(file):
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

        # Step 2: Replace all case-insensitive "IITM" with "IIT Madras"
        pattern = re.compile(r'IITM', re.IGNORECASE)
        for root, _, files in os.walk(extracted_dir):
            for file in files:
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8', newline='') as f:
                    content = f.read()
                replaced = pattern.sub("IIT Madras", content)
                with open(filepath, 'w', encoding='utf-8', newline='') as f:
                    f.write(replaced)
                    
        # Step 3: Concatenate all file contents (like `cat *`)
        combined = b""
        all_files = sorted(os.listdir(extracted_dir))
        for fname in all_files:
            fpath = os.path.join(extracted_dir, fname)
            if os.path.isfile(fpath):
                with open(fpath, 'rb') as f:
                    combined += f.read()

        # Step 4: Compute SHA-256 hash
        sha256_hash_value = hashlib.sha256(combined).hexdigest()
        print("✅ Result of `cat * | sha256sum`:", sha256_hash_value)

        # Return extracted file names and SHA-256 hash
        return sha256_hash_value

    except Exception as e:
        return {"error": str(e)}

    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)