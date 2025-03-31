import re
import parse

# Define patterns for extracting key parameters
regex_patterns = {
    "url": r"https?://[^\s]+",
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "filename": { "pattern": r"[A-Za-z0-9_.-]+\.(txt|md|json|jsonl|csv|pdf|xlsx)\b", "group": True },  # Extracts file names with specific extensions
    "zip_filename": r"\b[A-Za-z0-9_.-]+\.zip\b",  # Extracts ZIP file names
    "sheet_formula": r"=[A-Z]+\(.+\)",  # Google Sheets formulas
    "prettier_version": r"prettier@(\d+\.\d+\.\d+)",  # Matches versions like prettier@3.4.2
    "weekday": r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)s?\b",  # Extracts the day of the week
    "start_date": r"\b(\d{4}-\d{2}-\d{2})\b",  # Matches YYYY-MM-DD format (first occurrence = start date)
    "end_date": r"\b(\d{4}-\d{2}-\d{2})\b",  # Matches YYYY-MM-DD format (last occurrence = end date)
    "filter_date": r"\b[A-Za-z]{3} [A-Za-z]{3} \d{2} \d{4} \d{2}:\d{2}:\d{2} GMT[+-]\d{4}\b",  
    "filter_date_iso" : r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z\b",
    "cvs_column_name": r'"([^"]+)"\s+column',  # Extracts the column name from a CSV file
    "json_column_name": {"pattern": r'(\b\w+)(?= field\b)', "multiple": True},  # Extracts the field name from a JSON object
    "css_class_name": r'(\b\w+)(?= class\b)',  # Extracts the field name from a JSON object
    "html_element": r"<(\w+)>",  # Extracts HTML tags
    "modification_date": r"on or after\s+([\w,:\s]+IST)",
    "min_file_size": r"at least (\d+) bytes",
}

"""
Identifies the use case ID by checking if expected keywords are present.
"""
use_cases = {
    "GA1.1": ["Visual Studio Code", "install", "run", "enter"],
    "GA1.2": ["HTTPS request", "URL encoded", "email"],
    "GA1.3": ["npx", "prettier", "sha256sum"],
    "GA1.4": ["Google Sheets", "formula", "="],
    "GA1.5": ["Excel", "formula into Excel", "="],
    "GA1.6": ["hidden input", "secret value"],
    "GA1.7": ["days are there", "date range"],
    "GA1.8": ["CSV", "unzip", "column"],
    "GA1.9": ["sort", "JSON array", "array of objects", "field", "result", "tie"],
    "GA1.10": ["JSON", "convert", "hash", "multi-cursors"],
    "GA1.11": ["CSS selectors", "find", "sum", "data-value"],
    "GA1.12": ["files", "CSV", "encoding", "symbol", "values"],
    "GA1.13": ["GitHub", "repository", "commit", "JSON", "push", "raw", "url"],
    "GA1.14": ["case", "replace", "folder", "sha256sum", "cat", "bash"],
    "GA1.15": ["extract", "list", "files", "file size", "modified", "total size"],
    "GA1.16": ["extract", "move", "rename", "files", "digit", "sha256sum", "grep", "bash"],
    "GA1.17": ["extract", "identical", "same", "number", "different", "between"],
    "GA1.18": ["SQLite", "database", "table", "column", "SQL", "calculate", "ticket type"],
    
    "GA2.1": [ "documentation", "Markdown", "include", "heading"],
    "GA2.2": [ "image", "compress", "losslessly"],
    "GA2.3": [ "github", "publish", "page", "email", "url"],
    "GA2.4": [ "Google Colab", "email", "program", "access"],
    "GA2.5": [ "Google Colab", "image", "run", "code", "pixels" ],
    "GA2.6": [ "vercel", "python", "api", "deploy", "json", "request", "marks" ],
    "GA2.7": [ "github", "action", "steps", "email", "reposit" ],
    "GA2.8": [ "docker", "image", "tag", "url" ],
    "GA2.9": [ "fastapi", "api", "csv", "json", "serve", "student" ],
    "GA2.10": [ "llamafile", "ngrok", "run", "tunnel", "model" ],
    
    "GA3.1": [ "httpx", "post", "openai", "sentiment" ],
    "GA3.2": [ "openai", "number", "token", "request", "cost" ],
    "GA3.3": [ "openai", "chat", "completion", "json", "body", "api" ],
    "GA3.4": [ "openai", "extract", "json", "image", "api", "text", "base64", "url" ],
    "GA3.5": [ "openai", "json", "post", "api", "embeddings", "transaction", "messages" ],
    "GA3.6": [ "python", "cosine", "similar", "pair", "embeddings", "tuple" ],
    "GA3.7": [ "fastapi", "cosine", "json", "body", "similar", "embeddings", "api", "score" ],
    "GA3.8": [ "fastapi", "api", "execute", "query", "parameter", "extract", "json" ],
    "GA3.9": [ "LLM", "prompt", "say", "yes"],
    
    "GA4.1": [ "cricinfo", "batsman", "statistic", "page", "importhtml", "source", "sheet", "extract", "analysis", "ducks" ],
    "GA4.2": [ "imdb", "movie", "filter", "rating", "titles", "extract", "json" ],
    "GA4.3": [ "markdown", "api", "application", "Wikipedia", "heading", "endpoint", "content" ],
    "GA4.4": [ "weather", "api", "forecast", "query", "bbc", "extract", "locationid", "json" ],
    "GA4.5": [ "Nominatim", "api", "latitude", "geospatial", "minimum", "osm_id", "boundingbox" ],
    "GA4.6": [ "HNRSS", "Hacker", "news", "url", "topic", "filter", "result" ],
    "GA4.7": [ "github", "api", "profile", "endpoint", "follower", "criteria", "created_at", "iso" ],
    "GA4.8": [ "github", "action", "schedule", "cron", "workflow", "commit", "repository", "Trigger" ],
    "GA4.9": [ "extract", "pdf", "table", "cleaning", "filtering", "calculation" ],
    "GA4.10": [ "convert", "pdf", "markdown", "format", "submit", "Prettier" ],
    
    "GA5.1": [ "excel", "data", "clean", "extract", "normalize", "trim", "convert", "filter", "margin", "total", "sales", "cost" ],
    "GA5.2": [ "process", "text", "file", "unique", "students", "clean", "count", "dataset", "parse", "extract", "remove", "reliable" ],
    "GA5.3": [ "data", "analyst", "Scale Resources", "Content Planning", "Marketing Insights" ],
    "GA5.4": [ "Apache", "web", "log", "Filter the Log Entries", "Aggregate Data by IP", "Data Consumer" ],
    "GA5.5": [ "data", "analyst", "Sales Entries", "Mis-spelt City Names", "Aggregate Sales", "clustering" ],
    "GA5.6": [ "data", "recovery", "analyst", "Parse the Sales Data", "Data Validation and Cleanup", "Calculate Total Sales" ],
    "GA5.7": [ "data", "analyst", "Parse the Large, Nested JSON", "Count Key Occurrences", "Return the Count", "placeholder" ],
    "GA5.8": [ "data", "analyst", "Filter Posts by Date", "Evaluate Comment Quality", "Extract and Sort Post IDs", "post" ],
    "GA5.9": [ "YouTube", "link", "Access the Video", "Convert to Audio", "Transcribe the Segment" ],
    "GA5.10": [ "digital", "forensics", "analyst", "Understand the Mapping", "Reassemble the Image", "Output the Reconstructed Image", "scramble" ],
}

def extract_using_regex(text):
    """
    Extracts parameters dynamically using regex patterns.
    """
    extracted = {}
    for param, pattern in regex_patterns.items():
        if isinstance(pattern, str):
            matches = re.search(pattern, text)
            if matches:
                #extracted[param] = matches.group(0)
                extracted[param] = matches.groups()[0] if matches.groups() else matches.group()
        elif "multiple" in pattern and pattern["multiple"]:
            matches = re.findall(pattern["pattern"], text)  # Finds all occurrences
            if matches:
                extracted[param] = matches
        elif pattern["group"]:
            matches = re.search(pattern["pattern"], text)
            if matches:
                extracted[param] = matches.group()
    return extracted

def identify_use_case(text):
    for case_id, keywords in use_cases.items():
        if all(keyword.lower() in text.lower() for keyword in keywords):
            return case_id
    return "Unknown Use Case"

def extract_info(text):
    """
    Extracts use case ID and parameters from input text.
    """
    case_id = identify_use_case(text)
    regex_params = extract_using_regex(text)
    #parse_params = extract_using_parse(text, case_id)

    # Merge both extraction methods
    #extracted_params = {**regex_params, **parse_params}
    extracted_params = {**regex_params}

    return {"GA_No": case_id, "parameters": extracted_params}

# # Test Case
# input_text = """
# Let's make sure you know how to use npx and prettier.

# Download . In the directory where you downloaded it, make sure it is called README.md, and run npx -y prettier@3.4.2 README.md | sha256sum.

# What is the output of the command?
# """

# print(extract_info(input_text))

# text = "Send a HTTPS request to https://httpbin.org/get with the URL encoded parameter email set to 23f2004837@ds.study.iitm.ac.in"
# print(extract_info(text))