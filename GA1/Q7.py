import os, json, re
from datetime import datetime, timedelta

def execute(question: str, parameter):
    dates = extract_dates(question)
    start_date, end_date, target_day = parameter["start_date"], parameter["end_date"], parameter["weekday"]
    num_weekdays = count_weekdays_in_range(dates[0], dates[1], target_day)
    return num_weekdays
        
def count_weekdays_in_range(start_date_str, end_date_str, target_day):
    """
    Counts the number of a specific weekday (e.g., 'Wednesday') between two dates.

    Args:
        start_date_str (str): Start date in 'YYYY-MM-DD' format.
        end_date_str (str): End date in 'YYYY-MM-DD' format.
        target_day (str): Day of the week (e.g., 'Monday', 'Tuesday', etc.).

    Returns:
        int: Number of target days in the date range.
    """
    # Convert input strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Normalize dates to avoid time issues
    start_date = start_date.replace(hour=0, minute=0, second=0)
    end_date = end_date.replace(hour=0, minute=0, second=0)

    # Ensure start_date <= end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    # Initialize counter
    count = 0

    # Iterate through each day in the range
    current_date = start_date
    while current_date <= end_date:
        if current_date.strftime("%A") == target_day:
            count += 1
        current_date += timedelta(days=1)

    return count

def extract_dates(text):
    # Regex pattern to match YYYY-MM-DD format
    date_pattern = r"(\d{4}-\d{2}-\d{2})"
    
    # Find all matching dates
    matches = re.findall(date_pattern, text)
    
    # Return the first and last match if found
    return matches if matches else None