import os, json, re

def execute(question: str, parameter):
    json_payload = generate_text_embedding_payload(question)
    return json_payload
        
def generate_text_embedding_payload(question):
    # Extract all transaction codes and email addresses
    matches = re.findall(r"transaction code (\d+) sent to ([\w\.-]+@[\w\.-]+)", question)

    if not matches:
        return "Error: Could not extract transaction codes and email addresses."

    # Create a list of messages for the input key
    messages = [
        f"Dear user, please verify your transaction code {transaction_code} sent to {email_address}"
        for transaction_code, email_address in matches
    ]

    # Construct the final JSON payload
    json_payload = {
        "model": "text-embedding-3-small",
        "input": messages
    }

    return json.dumps(json_payload, indent=2)