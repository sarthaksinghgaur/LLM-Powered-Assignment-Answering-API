import os, json
from pathlib import Path
from request_context import current_request_var
import csv, shutil

def execute(question: str, parameter, file_bytes: None):
    
    if not file_bytes:
        return "No file provided"
    
    file = parameter["_file_"]
    
    FOLDER_PATH = Path(__file__).parent
    csv_path = os.path.join(FOLDER_PATH, "q-fastapi.csv")
    with open(csv_path, "wb") as buffer:
        file.file.seek(0)
        shutil.copyfileobj(file.file, buffer)
    
    request = request = current_request_var.get()
    base_url = str(request.base_url)
    # Check if the request is behind a proxy and use "https" if needed
    if request.headers.get("X-Forwarded-Proto") == "https":
        base_url = base_url.replace("http://", "https://")

    # Ensure base_url always ends with "/"
    if not base_url.endswith("/"):
        base_url += "/"
        
    return base_url + "fastapi/api"


def get_students(class_: list[str] = None):
    FILE_PATH = Path(__file__).parent / "q-fastapi.csv"
    students = read_csv(FILE_PATH)
    if class_:
        students = [student for student in students if student["class"] in class_]
    return {"students": students}
    
def read_csv(file_path):
    students = []
    with open(file_path, mode="r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            students.append({"studentId": int(row["studentId"]), "class": row["class"]})
    return students