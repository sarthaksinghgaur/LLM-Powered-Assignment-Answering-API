import os, json, requests, pandas as pd
from bs4 import BeautifulSoup
from reg_parserlib import extract_using_regex

def execute(question: str, parameter):
        print(f"File Name: {os.path.basename(__file__)[0]}")
        regex_patterns = {
            "pageNo": {"pattern": r"page number (\d+)", "multiple": True}
        }
        column_name = "0" # hardcoded for duck
        parameters = extract_using_regex(regex_patterns, question)
        if "pageNo" in parameters:
            page_number = int(parameters["pageNo"][-1])
            total_runs = sum_column_from_cricinfo_page("https://stats.espncricinfo.com/ci/engine/stats/index.html", page_number, column_name)
            return total_runs
        else:
            return 0

def sum_column_from_cricinfo_page(base_url: str, page_number: int, column_name: str) -> int:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }

    params = {
        "class": 2,  # ODI format
        "template": "results",
        "type": "batting",
        "page": page_number
    }

    # Step 1: Fetch the webpage
    response = requests.get(base_url, params=params, headers=HEADERS)
    if response.status_code != 200:
        print(f"⚠ Error: Failed to fetch page. Status Code: {response.status_code}")
        return 0

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", class_="engineTable")

    if len(tables) < 3:
        print("⚠ Error: Expected batting stats table not found.")
        return 0

    stats_table = tables[2]  # Usually the main player stats table

    headers = [th.text.strip() for th in stats_table.find_all("th")]
    if not headers:
        print("⚠ Error: No headers found.")
        return 0

    # Extract rows
    data_rows = stats_table.find_all("tr", class_="data1")
    data = []

    for row in data_rows:
        cells = [td.text.strip() for td in row.find_all("td")]
        if len(cells) == len(headers):
            data.append(cells)

    if not data:
        print("⚠ Error: No valid data rows.")
        return 0

    df = pd.DataFrame(data, columns=headers)

    # Find target column
    target_col = None
    for col in df.columns:
        if col.strip() == column_name.strip():
            target_col = col
            break

    if not target_col:
        print(f"❌ Column '{column_name}' not found in table.")
        print(f"📊 Available columns: {list(df.columns)}")
        return 0

    # Clean and convert column
    df[target_col] = df[target_col].replace({'–': '0', '-': '0', '': '0'}).astype(str)
    df[target_col] = pd.to_numeric(df[target_col], errors='coerce').fillna(0)

    total = int(df[target_col].sum())
    return total
