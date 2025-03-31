import os, json, gzip
import re
from datetime import datetime
from collections import defaultdict
from pathlib import Path

def execute(question: str, parameter, file_bytes = None):
    route_match = re.findall(r"requests under (\S+/)", question)
    route = route_match[-1] if route_match else None
    FILE_PATH = Path(__file__).parent / "s-anand.net-May-2024"
    top_consumer_data = find_top_data_consumer(FILE_PATH, route, parameter["start_date"])
    return top_consumer_data
        

def find_top_data_consumer(log_file, target_path, target_date):
    """Finds the IP address that downloaded the most data for the given criteria."""
    target_path2 = "/"+target_path
    max_downloaded_bytes = 0
    data_usage = defaultdict(int)  # Dictionary to store total data per IP
    with open(log_file, "rt", encoding="utf-8") as file:
        for line in file:
            log_entry = parse_log_line(line)
            if not log_entry:
                continue

            # Extract date from timestamp
            timestamp_str = log_entry["timestamp"].split()[0]  # Remove timezone offset
            log_time = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S")
            log_date_str = log_time.strftime("%Y-%m-%d")  # Convert to YYYY-MM-DD format

            # Check if request matches criteria
            if (log_date_str == target_date
                and (log_entry["url"].startswith(target_path) or log_entry["url"].startswith(target_path2))
                and 200 <= int(log_entry["status"]) < 300):  # Successful request

                data_usage[log_entry["ip"]] += log_entry["size"]

    # Find the top IP address by data volume
    if data_usage:
        top_ip = max(data_usage, key=data_usage.get)
        max_downloaded_bytes = data_usage[top_ip]
        print(f"\n🏆 Top Data Consumer: {top_ip}")
        print(f"📦 Total Data Downloaded: {max_downloaded_bytes:,} bytes")
    else:
        print("\n⚠️ No matching records found!")

    return max_downloaded_bytes

def parse_log_line(line):
    """Parses a single line from the Apache log file and extracts key fields."""

    log_pattern = (
        r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>.*?)\] '
        r'"(?P<method>\S+) (?P<url>\S+) (?P<protocol>.*?)" '
        r'(?P<status>\d+) (?P<size>\S+) .*'
    )

    match = re.match(log_pattern, line)
    if match:
        log_entry = match.groupdict()
        log_entry["size"] = int(log_entry["size"]) if log_entry["size"].isdigit() else 0
        return log_entry
    return None