import os, json, subprocess, hashlib, io
import tempfile, shutil

def execute(question: str, parameter, file_bytes: None):
    #file_bytes = file_bytes.decode()
    
    temp_dir = tempfile.mkdtemp()
    try:
        file = parameter["_file_"]
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as buffer:
            file.file.seek(0)
            shutil.copyfileobj(file.file, buffer)
        
        # Execute Prettier on the file
        prettier_process = subprocess.run(
            f"npx -y prettier@3.4.2 {file_path}",
            shell=True,
            capture_output=True,
            text=True
        )

        # Get formatted output
        formatted_output = prettier_process.stdout

        # Compute SHA-256 manually
        sha256_hash = hashlib.sha256(formatted_output.encode()).hexdigest()

        print("SHA-256:", sha256_hash)

        return sha256_hash
    finally:
    # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)