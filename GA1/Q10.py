import os, json, io
import hashlib

def execute(question: str, parameter, file_bytes):
    if file_bytes is None:
        return "Error: No file uploaded"
    data = {}
    file = parameter["_file_"]
    file.file.seek(0)
    for line in file.file:
        line = line.strip().decode("utf-8")
        if '=' in line:
            key, value = line.split('=', 1)
            data[key] = value
    
    # file_obj = io.BytesIO(file_bytes)
    # for line in file_obj:
    #     line = str(line.strip())
    #     if '=' in line:
    #         key, value = line.split('=', 1)
    #         data[key] = value
    json_string = json.dumps(data, sort_keys=True)
    json_hash = hashlib.sha256(json_string.encode("utf-8")).hexdigest()
    return hash_object(json_string), json_hash, data
    # json_output, hash_output = convert_and_hash(file_bytes)
    # return hash_output, json_output

def hash_object(data: dict) -> str:
    """Hashes a dictionary using SHA-256."""
    json_string = json.dumps(data, sort_keys=True, separators=(",", ":"))  # Ensure consistent ordering
    hash_object = hashlib.sha256(json_string.encode("utf-8"))
    return hash_object.hexdigest()
        
def convert_and_hash(file_bytes):
    data = {}
    file_obj = io.BytesIO(file_bytes)
    for line in file_obj:
        line = str(line.strip())
        if '=' in line:
            key, value = line.split('=', 1)
            data[key] = value

    json_string = json.dumps(data, sort_keys=True)
    json_hash = hashlib.sha256(json_string.encode("utf-8")).hexdigest()
    return data, json_hash