import os, json, base64, io
from PIL import Image

def execute(question: str, parameter, file_bytes):
    # file_io = io.BytesIO(file_bytes)  # Convert bytes to a file-like object
    # image = Image.open(file_io)  
    json_body = generate_json_body_from_image_file(file_bytes, parameter["file_extention"], model="gpt-4o-mini")
    return json_body

def generate_json_body_from_image_file(file_bytes, file_ext, model="gpt-4o-mini"):
    try:
        # Convert to base64
        base64_image = base64.b64encode(file_bytes).decode('utf-8')
        mime_types = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'webp': 'image/webp'
        }
        mime_type = mime_types.get(file_ext, 'image/jpeg')

        # Construct the JSON body
        return {
            "model": model,  # Using "gpt-4o-mini" as specified
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract text from this image"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1000  # Adjust as needed
        }

    except Exception as e:
        return {"error": str(e)}
