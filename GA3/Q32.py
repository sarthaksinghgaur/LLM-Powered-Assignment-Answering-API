import os, json, re
import tiktoken

def execute(question: str, parameter):
    token_usage = estimate_token_usage(question)
    return token_usage    
        
def estimate_token_usage(question):
    user_message = extract_user_message(question)
    # Load the tokenizer for GPT-4o-Mini
    enc = tiktoken.encoding_for_model("gpt-4o")  # GPT-4o-Mini uses the same encoding

    # Get the token count using tiktoken
    token_count = len(enc.encode(user_message))+7

    return token_count

def extract_user_message(text):
    match = re.search(r"user message:\s*(.*?)\s*\.\.\. how many", text, re.DOTALL)
    return match.group(1) if match else None