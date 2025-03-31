import os, json, pdfplumber, re, pandas as pd, io
from reg_parserlib import extract_using_regex
import tabula

from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from typing import Optional

def execute(question: str, parameter, file_bytes):
        print(f"File Name: {os.path.basename(__file__)[0]}")
        
        pdf_bytes = file_bytes
        pdf_file = io.BytesIO(pdf_bytes)
        
        df = extract_data_from_pdf_tabula(pdf_file)
        #df.to_csv("data.csv", index=False)
        subject1, marks, subject2, marks_range = get_parameters(question)
        
        # verify subject parameters
        total_marks = filter_and_calculate(df, marks_range, subject2, marks, subject1)
        
        return total_marks

def extract_data_from_pdf_tabula(pdf_file):
    tables = tabula.read_pdf(pdf_file, pages="all", multiple_tables=True)

    # Initialize an empty list to store all DataFrames
    all_dfs = []

    # Iterate through each table and add a "Group" column based on the page number
    for i, table in enumerate(tables):
        # Add a "Group" column to the table
        table["Group"] = i + 1  # Group 1 for Page 1, Group 2 for Page 2, etc.
        # Append the table to the list
        all_dfs.append(table)

    # Combine all DataFrames into a single DataFrame
    df = pd.concat(all_dfs, ignore_index=True)

    # Rename columns for easier access (if necessary)
    df.columns = ["Maths", "Physics", "English", "Economics", "Biology", "Group"]

    # Convert marks to numerical data types
    df["Maths"] = pd.to_numeric(df["Maths"], errors="coerce")
    df["Physics"] = pd.to_numeric(df["Physics"], errors="coerce")
    df["English"] = pd.to_numeric(df["English"], errors="coerce")
    df["Economics"] = pd.to_numeric(df["Economics"], errors="coerce")
    df["Biology"] = pd.to_numeric(df["Biology"], errors="coerce")
    df["Group"] = pd.to_numeric(df["Group"], errors="coerce")

    # Drop rows with missing values (if any)
    df.dropna(inplace=True)

    # # Display the first few rows of the combined DataFrame
    # print(df.head())

    # # Display the data types of the columns
    # print(df.dtypes)
    # filtered_df = df[(df["Physics"] >= 56) & (df["Group"].between(46, 79))]

    # total_biology_marks = filtered_df["Economics"].sum()
    # print(total_biology_marks)
    return df
    
def extract_data_from_pdf(pdf_path):
    data = []
    group_number = None  # Track the current group number
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                tables = page.extract_tables()

                # Detect group number
                group_match = re.search(r"Group\s+(\d+)", text)
                if group_match:
                    group_number = int(group_match.group(1))

                for table in tables:
                    for row in table:
                        if len(row) == 5 and group_number is not None:
                            clean_row = [group_number] + [cell.strip() if cell else "0" for cell in row]
                            data.append(clean_row)

        df = pd.DataFrame(data, columns=["Group", "Maths", "Physics", "English", "Economics", "Biology"])
        df = df.apply(pd.to_numeric, errors="coerce")
        df = df.dropna()

        return df
    except Exception as e:
        print(f"Error: {e}")

def filter_and_calculate(df, group_range, filter_subject, min_marks, target_subject):
    # Filter students based on marks in the filter_subject and group range
    df_filtered = df[
        (df["Group"].between(group_range[0], group_range[1])) &
        (df[filter_subject] >= min_marks)
    ]

    # Calculate the total target_subject marks
    total = df_filtered[target_subject].sum().item()
    return total
        
# def extract_data_from_pdf(pdf_path):
#     data = []
#     group_number = None  # Track the current group number

#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text = page.extract_text()  # Extract text to detect groups
#             tables = page.extract_tables()  # Extract tables

#             # Detect group number from the text
#             group_match = re.search(r"Group\s+(\d+)", text)
#             if group_match:
#                 group_number = int(group_match.group(1))  # Extract numeric group number

#             for table in tables:
#                 for row in table:
#                     # Ensure the row contains valid marks (should have 5 values)
#                     if len(row) == 5 and group_number is not None:
#                         clean_row = [group_number] + [cell.strip() if cell else "0" for cell in row]
#                         data.append(clean_row)

#     # Convert extracted data into a Pandas DataFrame
#     df = pd.DataFrame(data, columns=["Group", "Maths", "Physics", "English", "Economics", "Biology"])

#     # Convert numeric columns
#     df = df.apply(pd.to_numeric, errors="coerce")

#     # Drop any rows with missing values
#     df = df.dropna()

#     return df

# def filter_and_calculate(df, group_range, subject, subject2, min_marks):
#     # Filter data based on user input
#     df_filtered = df[(df["Group"].between(group_range[0], group_range[1])) & (df[subject2] >= min_marks)]

#     # Calculate the total marks for the selected subject
#     total_marks = df_filtered[subject].sum()

#     return df_filtered, total_marks

def get_parameters(question):

    # What is the total Economics marks of students who scored 56 or more marks in Maths in groups 53-86 (including both groups)?
    regex_patterns = {
        "location": {"pattern": r"What is the total ([\w\s]+) marks of students who scored (\d+)  or more marks in ([\w\s]+) in groups (\d+)-(\d+) ", "multiple": True}
    }
    reg_params = extract_using_regex(regex_patterns, question)
    subject1 = reg_params["location"][-1][0] if "location" in reg_params else "Economics"
    marks = int(reg_params["location"][-1][1]) if "location" in reg_params else 56
    subject2 = reg_params["location"][-1][2] if "location" in reg_params else "Maths"
    marks_range = (int(reg_params["location"][-1][3]), int(reg_params["location"][-1][4])) if "location" in reg_params else (53, 86)
    return subject1, marks, subject2, marks_range