import os, json, io

def execute(question: str, parameter, file_bytes):
    json_file = io.BytesIO(file_bytes)
    #json.loads(json_file.read())
    
    return sort_json_array(json_file.read(), parameter["json_column_name"][0], parameter["json_column_name"][1])
    
        
def sort_json_array(json_str, sort_by, tie_breaker):
    try:
        data = json.loads(json_str)
        # Sort by sort_by, then by tie_breaker
        sorted_data = sorted(data, key=lambda x: (x[sort_by], x[tie_breaker]))
        return json.dumps(sorted_data, separators=(',', ':'))
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"Invalid input: {str(e)}")