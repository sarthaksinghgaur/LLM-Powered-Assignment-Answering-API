import os, json, io, re

def execute(question: str, parameter, file_bytes):
        print(f"File Name: {os.path.basename(__file__)[0]}")
        
        unique_students = extract_student_ids(file_bytes)
        unique_count = len(unique_students)
        return unique_count
        
def extract_student_ids(file_bytes):
    """
    Reads the file line by line and extracts student IDs.

    Args:
        file_path (str): The path of the student data file.

    Returns:
        set: A set of unique student IDs.
    """
    unique_students = set()
    total_lines = 0
    
    memory_file = io.StringIO(file_bytes.decode("utf-8"))  
    lines = memory_file.readlines()
    pattern = r'([A-Z0-9]{10})'

    try:
        for line in lines:
            total_lines += 1
            line = line.strip()  # Remove leading/trailing spaces

            if not line:  # Skip empty lines
                continue

            #match = re.search(pattern, line)
            match = re.search(r"-\s*([A-Z0-9]+)\s*(?=::|Marks|$)", line)
            if match:
                student_id = match.group(1)
                if student_id:  # Ensure it's not an empty string
                    unique_students.add(student_id)

        #print(f"\n📊 Total Lines Read: {total_lines}")
        #print(f"🔍 Sample Extracted IDs: {list(unique_students)}")  # Show first 10 IDs for verification

    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return set()

    return unique_students