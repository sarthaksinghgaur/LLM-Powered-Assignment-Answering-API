import os, json, requests
from reg_parserlib import extract_using_regex

def execute(question: str, parameter):
        print(f"File Name: {os.path.basename(__file__)[0]}")
        location, min_followers = get_location_followers(question)
        
        users = get_github_users(location, min_followers)
        return users
        
def get_github_users(location="Hydrabad", min_followers=50):
    url = "https://api.github.com/search/users"
    params = {
        "q": f"location:{location} followers:>{min_followers}",
        "sort": "joined",
        "order": "desc",
        "per_page": 100  # Max results per page
    }
    headers = {"Accept": "application/vnd.github.v3+json"}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        users = response.json().get("items", [])
        if users:
            newest_user = users[0]  # The first user in the sorted list is the newest
            user_details = requests.get(newest_user["url"], headers=headers).json()
            return user_details["created_at"]  # ISO 8601 format
        else:
            return "No users found with the given criteria."
    else:
        return f"Error: {response.status_code}, {response.text}"
    
def get_location_followers(text):
    regex_patterns = {
        "location": {"pattern": r"find all users located in the city ([\w\s]+) with over (\d+) followers.", "multiple": True}
    }
    reg_params = extract_using_regex(regex_patterns, text)
    location = reg_params["location"][-1][0] if "location" in reg_params else "Singapore"
    min_followers = int(reg_params["location"][-1][1]) if "location" in reg_params else 190

    return location, min_followers