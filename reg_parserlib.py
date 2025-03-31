import re

def extract_using_regex(regex_patterns, text):
    """
    Extracts parameters dynamically using regex patterns.
    """
    extracted = {}
    for param, pattern in regex_patterns.items():
        if isinstance(pattern, str):
            matches = re.search(pattern, text)
            if matches:
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