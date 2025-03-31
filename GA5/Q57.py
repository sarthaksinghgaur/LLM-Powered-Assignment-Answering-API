import os, json, io, re

def execute(question: str, parameter, file_bytes = None):
    if file_bytes is None:
        return " No file provided"
    target_key = get_target_key(question)
    key_count = count_key_in_json(io.BytesIO(file_bytes), target_key)
    
    return key_count
        
def count_key_in_json(file, target_key):
    
    data = json.load(file)

    # Recursive function to count occurrences of the target key
    def count_key_occurrences(obj, target_key):
        count = 0
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == target_key:
                    count += 1
                count += count_key_occurrences(value, target_key)
        elif isinstance(obj, list):
            for item in obj:
                count += count_key_occurrences(item, target_key)
        return count

    # Count occurrences of the target key
    return count_key_occurrences(data, target_key)

def get_target_key(question):
    matches = re.findall(r"(\S+) appear as a key", question)
    # Take the last key if there are multiple matches
    last_key = matches[-1] if matches else None
    return last_key