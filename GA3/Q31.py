import os, json, re

def execute(question: str, parameter):
    generated_code = generate_sentiment_analysis_code(question)
    return generated_code
        
def generate_sentiment_analysis_code(question):
    # Extract the meaningless text from the question
    #match = re.search(r"One of the test cases involves sending a sample piece of meaningless text:\s*([\s\S]+?)\nWrite a Python program", question)
    match = re.search(r"One of the test cases involves sending a sample piece of meaningless text:\s*([\s\S]+?)\s*Write a Python program", question)

    if not match:
        return "Error: Could not extract the meaningless text."

    test_text = match.group(1).strip()

    # Generate the required Python code
    code = f'''import httpx

    def analyze_sentiment():
        url = "https://api.openai.com/v1/chat/completions"
        headers = {{
            "Authorization": "Bearer dummy_api_key",
            "Content-Type": "application/json"
        }}
        data = {{
            "model": "gpt-4o-mini",
            "messages": [
                {{"role": "system", "content": "Analyze the sentiment of the given text and classify it as GOOD, BAD, or NEUTRAL."}},
                {{"role": "user", "content": "{test_text}"}}
            ]
        }}

        response = httpx.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        return result
        
    analyze_sentiment()
'''

    return code