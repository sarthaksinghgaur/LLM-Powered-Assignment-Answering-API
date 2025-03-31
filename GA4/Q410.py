import os, json

def execute(question: str, parameter):
        print(f"File Name: {os.path.basename(__file__)[0]}")
        return {
            "GA_No": {os.path.basename(__file__)},
            "parameters": parameter
        }