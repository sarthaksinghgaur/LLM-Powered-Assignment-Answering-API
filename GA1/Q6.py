import os, json
from bs4 import BeautifulSoup
import tempfile, shutil

def execute(question: str, parameter, file_bytes: None):
    if file_bytes is None:
        return "No file provided."
    else:
        temp_dir = tempfile.mkdtemp()
        try:
            file = parameter["_file_"]
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as buffer:
                file.file.seek(0)
                shutil.copyfileobj(file.file, buffer)
            
            return extract_hidden_input_value(file_path)
        finally:
            # Clean up temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)
        
def extract_hidden_input_value(filename):

    # Read the HTML file
    with open(filename, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the first hidden input and get its value
    hidden_input = soup.find('input', {'type': 'hidden'})
    return hidden_input.get('value')