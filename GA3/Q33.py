import os, json, re

def execute(question: str, parameter):
    json_body_string_friend = generate_json_body(question)
    return json_body_string_friend
    
def generate_json_body(question):
    # Extract the model name from the question
    model_match = re.search(r"Uses model (\S+)", question)
    if not model_match:
        return "Error: Could not extract the model name."
    model_name = model_match.group(1)

    # Extract the system message from the question
    system_message_match = re.search(r"Has a system message: (.*)", question)
    if not system_message_match:
        return "Error: Could not extract the system message."
    system_message = system_message_match.group(1).strip()

    # Extract the user message from the question
    user_message_match = re.search(r"Has a user message: (.*)", question)
    if not user_message_match:
        return "Error: Could not extract the user message."
    user_message = user_message_match.group(1).strip()

    # Extract the required fields for the JSON schema
    fields_match = re.search(r"with required fields: (.*?)(?:\.|$)", question)
    if not fields_match:
        return "Error: Could not extract the required fields."

    # Extract and clean required fields using regex to match all field definitions
    fields_text = fields_match.group(1)
    field_pattern = r"(\w+)\s*\((\w+)\)"  # Matches "field_name (type)"

    properties = {}
    required_fields = []

    for match in re.finditer(field_pattern, fields_text):
        field_name, field_type = match.groups()
        required_fields.append(field_name)

        # Map field type to JSON Schema type
        json_type = {
            "string": "string",
            "number": "number",
            "array": "array",
            "boolean": "boolean"
        }.get(field_type.lower(), None)

        if json_type is None:
            return f"Error: Unsupported field type '{field_type}' for field '{field_name}'."

        properties[field_name] = {"type": json_type}

    if not required_fields:
        return "Error: No valid required fields found."

    # Construct the JSON schema dynamically
    schema = {
        "type": "object",
        "properties": {
            "addresses": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": properties,
                    "required": required_fields,
                    "additionalProperties": False
                }
            }
        },
        "required": ["addresses"],
        "additionalProperties": False
    }

    # Construct the JSON body
    json_body = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "Respond in JSON"},
            {"role": "user", "content": "Generate 10 random addresses in the US"}
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "address_schema",
                "schema": schema,
                "strict": True
            }
        }
    }

    # Return the JSON body as a string with double quotes and indentation
    return json_body
    #return json.dumps(json_body, indent=2)