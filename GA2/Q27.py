import os, json, requests

def execute(question: str, parameter):
    
    repo_name = run_git_workflow(parameter["email"])
    return repo_name
    
def run_git_workflow(email):

    # GitHub repository details
    GITHUB_OWNER = "23f2004837"  # Replace with your GitHub username/org
    GITHUB_REPO = "daily-commit"   # Replace with your repo name
    WORKFLOW_FILE = "CV1.yml"  # Name of your workflow file
    BRANCH = "main"  # Branch to run the workflow on

    # Personal Access Token (PAT) with `repo` scope
    GITHUB_TOKEN = "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"  # Replace with your actual token

    # GitHub API endpoint
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"

    # API request headers
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }

    # Request body
    # Request body with input parameter
    payload = {
        "ref": BRANCH,  
        "inputs": {
            "email": email
        }
    }
    # Trigger the workflow
    response = requests.post(url, json=payload, headers=headers)

    # Print response status
    if response.status_code == 204:
        print("✅ Workflow triggered successfully!")
    else:
        print(f"❌ Failed to trigger workflow: {response.status_code}")
        print(response.text)
    
    return f"https://github.com/23f2004837/daily-commit"