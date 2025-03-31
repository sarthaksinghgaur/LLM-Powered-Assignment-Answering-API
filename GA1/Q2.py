import os, json, requests

def execute(question: str, parameter):
    # URL and parameters
    url = parameter["url"]
    params = {"email": parameter["email"]}
    # Make the GET request
    response = requests.get(url, params=params)
    return response.text