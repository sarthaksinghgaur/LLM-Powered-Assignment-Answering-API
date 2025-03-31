import os, json, io
from bs4 import BeautifulSoup

def execute(question: str, parameter, file_bytes):
    sum = sum_data_values(file_bytes, parameter['css_class_name'])
    return sum
        
def sum_data_values(file_bytes, target_class):
    file = io.StringIO(file_bytes.decode("utf-8"))
    soup = BeautifulSoup(file, 'html.parser')

    # Find all divs where 'foo' appears in the class list
    divs = soup.find_all('div', class_=lambda x: x and target_class in x.split())
    total = 0.0

    for div in divs:
        data_value = div.get('data-value')
        if data_value:
            try:
                total += float(data_value)
            except (ValueError, TypeError):
                continue

    return int(total)