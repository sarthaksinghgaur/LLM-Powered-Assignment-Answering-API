import os, json, re
from datetime import datetime
import pytz
from pathlib import Path

def execute(question: str, parameter, file_bytes = None):
    
    #print(f"File Name: {os.path.basename(__file__)[0]}")
    FILE_PATH = Path(__file__).parent / "s-anand.net-May-2024"
    
    page, from_hour, to_hour, day = get_filter_parameters(question)
    #s-anand.net-May-2024
    count = count_successful_requests(FILE_PATH, page, from_hour, to_hour, day)   
    return count
        

# Function to parse log lines
def parse_log_line(line):
    """Parses a single line from the Apache log file and extracts key fields."""

    log_pattern = (
        r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>.*?)\] '
        r'"(?P<method>\S+) (?P<url>\S+) (?P<protocol>.*?)" '
        r'(?P<status>\d+) (?P<size>\S+) .*'
    )

    match = re.match(log_pattern, line)
    if match:
        return match.groupdict()
    return None

# Function to check if a request meets the criteria
def is_valid_request(log_entry, target_path, start_hour, end_hour, day):
    """Checks if the log entry matches the GET request criteria."""

    try:
        # Convert log timestamp to a datetime object
        timestamp_str = log_entry["timestamp"].split()[0]  # Remove timezone offset
        log_time = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S")

        # # Convert to required timezone (GMT-0500 is EST)
        # est = pytz.timezone("America/New_York")
        # log_time = log_time.replace(tzinfo=pytz.utc).astimezone(est)

        # Check if it's a Friday within the required hours
        if (log_time.weekday() == day  # Friday (0=Monday, 4=Friday)
            and start_hour <= log_time.hour < end_hour
            and log_entry["method"] == "GET"
            and target_path.lower() in log_entry["url"].lower()
            and 200 <= int(log_entry["status"]) < 300):  # Successful request
            #print(log_entry)
            return True
    except Exception:
        return False

    return False

# Function to process the log file
def count_successful_requests(log_file, target_path, start_hour, end_hour, day):
    """Counts the number of successful GET requests based on criteria."""
    count = 0
    with open(log_file, "rt", encoding="utf-8") as file:
        for line in file:
            log_entry = parse_log_line(line)
            if log_entry and is_valid_request(log_entry, target_path, start_hour, end_hour, day):
                count += 1

    print(f"\n✅ Total Successful GET Requests for '{target_path}' on Fridays between {start_hour}:00 and {end_hour}:00 → {count}")
    return count

def day_to_number(day_name):
    """Convert day name to day number (Monday=0, Sunday=6)."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Mondays", "Tuesdays", "Wednesdays", "Thursdays", "Fridays", "Saturdays", "Sundays"]
    return days.index(day_name) % 7 if day_name in days else None

def get_filter_parameters(question):
    page_matches = re.findall(r"pages under (\S+)", question)
    from_matches = re.findall(r"from (\d{1,2}:\d{2})", question)
    until_matches = re.findall(r"until before (\d{1,2}:\d{2})", question)
    day_matches = re.findall(r"on (\w+)\??$", question)

    # Take the last occurrence if multiple matches exist
    page = page_matches[-1] if page_matches else None
    from_hour = int(from_matches[-1].split(":")[0]) if from_matches else None  # Convert "7:00" → 7
    to_hour = int(until_matches[-1].split(":")[0]) if until_matches else None  # Convert "9:00" → 9
    day = day_to_number(day_matches[-1]) if day_matches else None
    return page, from_hour, to_hour, day