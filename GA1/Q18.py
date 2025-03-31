import os, json, re

def execute(question: str, parameter):
    ticket_type = get_ticket_type(question)
    sql = generate_sql_for_ticket_type(ticket_type)
    return sql
        
def generate_sql_for_ticket_type(ticket_type: str):

    sql = f"""
SELECT SUM(units * price)
FROM tickets
WHERE lower(trim(type)) = LOWER('{ticket_type}');
""".strip()

    print("\n📄 Generated SQL query:")
    print(sql)
    return sql

def get_ticket_type(question: str):
    matches = re.findall(r'"([^"]+)" ticket type', question)
    # Take the last ticket type if there are multiple matches
    ticket_type = matches[-1] if matches else None
    return ticket_type
