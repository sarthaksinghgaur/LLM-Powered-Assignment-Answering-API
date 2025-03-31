import os, json
from request_context import current_request_var
from openai import OpenAI

def execute(question: str, parameter):
    request = request = current_request_var.get()
    base_url = str(request.base_url)

    # Check if the request is behind a proxy and use "https" if needed
    if request.headers.get("X-Forwarded-Proto") == "https":
        base_url = base_url.replace("http://", "https://")

    # Ensure base_url always ends with "/"
    if not base_url.endswith("/"):
        base_url += "/"
    return base_url + "execute"


function_definitions = [
    {
        "name": "get_ticket_status",
        "description": "Get the status of an IT support ticket.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {"type": "integer"}
            },
            "required": ["ticket_id"]
        }
    },
    {
        "name": "schedule_meeting",
        "description": "Schedule a meeting in a specific room at a given date and time.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "format": "date"},
                "time": {"type": "string", "format": "time"},
                "meeting_room": {"type": "string"}
            },
            "required": ["date", "time", "meeting_room"]
        }
    },
    {
        "name": "get_expense_balance",
        "description": "Retrieve the current expense reimbursement balance for an employee.",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {"type": "integer"}
            },
            "required": ["employee_id"]
        }
    },
    {
        "name": "calculate_performance_bonus",
        "description": "Calculate the performance bonus for a given employee in a specific year.",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {"type": "integer"},
                "current_year": {"type": "integer"}
            },
            "required": ["employee_id", "current_year"]
        }
    },
    {
        "name": "report_office_issue",
        "description": "Report an office issue to a specific department.",
        "parameters": {
            "type": "object",
            "properties": {
                "issue_code": {"type": "integer"},
                "department": {"type": "string"}
            },
            "required": ["issue_code", "department"]
        }
    }
]


your_api_key = "2NsEK91rAoRkHdYvCqvzT3BlbkFJsjU12SaEqybowZlDIo4hBJXa8XEOT6cUwFHa2RcPhVLjCF8zfQBLTl3e_q2XJlI10N-P_m72gA" 
client = OpenAI(api_key=your_api_key)

def parse_llm_task(q: str):
    #print(q)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a function classifier that extracts structured parameters from queries."},
            {"role": "user", "content": q}
        ],
        tools=[
            {
                "type": "function",
                "function": function
            } for function in function_definitions
        ],
        tool_choice="auto" 
    )

    message = response.choices[0].message
    if message.tool_calls:
        function_call = message.tool_calls[0]
        return {
            "name": function_call.function.name,
            "arguments": function_call.function.arguments
        }
    
    return {"error": "No matching function found"}




