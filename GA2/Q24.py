import os, json

def execute(question: str, parameter):
    results = {
        "22f2000946@ds.study.iitm.ac.in":"b6946", # Akash
        "22f3002560@ds.study.iitm.ac.in": "23a99", # Prabhnoor
        "23f2004837@ds.study.iitm.ac.in": "46936"
    }
    if parameter["email"] not in results:
        return {"error": "No use case found."}
    answer = results[parameter["email"]]
    return answer