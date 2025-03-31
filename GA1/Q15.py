import os, json, re, pytz
import zipfile
import shutil
import tempfile
import hashlib
from datetime import datetime

def execute(question: str, parameter, file_bytes: None):
    min_bytes = int(parameter["min_file_size"])
    cutoff_datetime = get_filter_date(parameter)
    return list_files_and_attributes(parameter["_file_"], cutoff_datetime, min_bytes)
        
def list_files_and_attributes(file, cutoff_datetime, min_bytes):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Save uploaded ZIP file
        zip_path = os.path.join(temp_dir, file.filename)
        with open(zip_path, "wb") as buffer:
            file.file.seek(0)
            shutil.copyfileobj(file.file, buffer)

        # # Extract ZIP file
        # extracted_dir = os.path.join(temp_dir, "extracted")
        # os.makedirs(extracted_dir, exist_ok=True)

        # with zipfile.ZipFile(zip_path, "r") as zip_ref:
        #     zip_ref.extractall(extracted_dir)
        
        total_size = 0

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                # Convert DOS date/time to datetime object
                file_datetime = datetime(
                    file_info.date_time[0],  # year
                    file_info.date_time[1],  # month
                    file_info.date_time[2],  # day
                    file_info.date_time[3],  # hour
                    file_info.date_time[4],  # minute
                    file_info.date_time[5]   # second
                )

                # Check if file meets criteria
                if (file_info.file_size >= min_bytes and
                    file_datetime >= cutoff_datetime):
                    total_size += file_info.file_size

        return total_size
        
    except Exception as e:
        return {"error": str(e)}

    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)
        
def get_filter_date(parameter):
    date_str = parameter["modification_date"]
    date_format = "%a, %d %b, %Y, %I:%M %p"

    # Parse to datetime (without timezone)
    dt_naive = datetime.strptime(date_str[:-4], date_format)  # Remove " IST"

    # # Convert to timezone-aware datetime (IST = UTC+5:30)
    # ist = pytz.timezone("Asia/Kolkata")
    # dt_ist = ist.localize(dt_naive)
    return dt_naive