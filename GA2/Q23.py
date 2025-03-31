import os, json


def execute(question: str, parameter):
  #return gitPortfolio(parameter["email"])
  cache = {
    "23f2004837@ds.study.iitm.ac.in": "https://23f2004837.github.io/",
    "21f2000588@ds.study.iitm.ac.in": "https://digvijaysinhchudasamaiitm.github.io/my-portfolio/",
    "24f2006749@ds.study.iitm.ac.in": "https://sakshi6749.github.io/portf/",
    "22f3002188@ds.study.iitm.ac.in": "https://22f3002188.github.io/portfolio/",
    "22f2001590@ds.study.iitm.ac.in": "https://22f2001590.github.io/TDS_GA2_page/"
  }
  if parameter["email"] not in cache:
    return {"Enter the value in url_cache"}
  
  return cache[parameter["email"]]
    
def gitPortfolio(email):
  return f"https://akashkunwar.github.io/TDS-portfolio/?email={email}"


# def extract_email_from_question(question: str) -> str:
#     """
#     Extracts the email address from the input question using regex.

#     Args:
#         question (str): The input question containing the email.

#     Returns:
#         str: The extracted email address.

#     Raises:
#         ValueError: If no email address is found in the question.
#     """
#     regex_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
#     match = re.search(regex_pattern, question)
#     if match:
#         return match.group(0).strip()
#     else:
#         raise ValueError("Email could not be extracted from the question.")

# def publish_github_pages_with_email(question: str):
#     """
#     Publishes a GitHub Pages site showcasing work with the email address extracted from the question.

#     Args:
#         question (str): The input question containing the email.

#     Returns:
#         str: The URL of the published GitHub Pages site.
#     """
#     # Extract email from the question
#     email = extract_email_from_question(question)

#     # GitHub username and token (fixed values)
#     username = "User_name"  # Replace with actual GitHub username
#     github_token = "git_token"  # Replace with your GitHub token

#     # Repository name
#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#     repo_name = f"github-pages-{timestamp}"

#     print(f"🔧 Creating GitHub repository: {repo_name}")
#     response = requests.post(
#         "https://api.github.com/user/repos",
#         headers={
#             "Authorization": f"token {github_token}",
#             "Accept": "application/vnd.github.v3+json"
#         },
#         json={"name": repo_name, "private": False}
#     )
#     if response.status_code not in [200, 201]:
#         raise Exception(f"Failed to create repo: {response.text}")

#     print("Repository created.")

#     # Create a temporary directory for the repository
#     temp_dir = tempfile.mkdtemp()

#     # Clone the repository using GitPython
#     clone_url = f"https://{username}:{github_token}@github.com/{username}/{repo_name}.git"
#     repo = Repo.clone_from(clone_url, temp_dir)

#     # Create an index.html file with the obfuscated email
#     html_content = f"""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>My Work</title>
#     </head>
#     <body>
#         <h1>Welcome to My GitHub Pages</h1>
#         <p>Contact me at: <!--email_off-->{email}<!--/email_off--></p>
#     </body>
#     </html>
#     """
#     with open(os.path.join(temp_dir, "index.html"), "w") as f:
#         f.write(html_content)

#     # Commit and push the changes using GitPython
#     repo.git.add(A=True)
#     repo.index.commit("Add GitHub Pages site with obfuscated email")
#     origin = repo.remote(name="origin")
#     origin.push()

#     print("Committed and pushed HTML file.")

#     # Enable GitHub Pages
#     print("Enabling GitHub Pages...")
#     pages_response = requests.post(
#         f"https://api.github.com/repos/{username}/{repo_name}/pages",
#         headers={
#             "Authorization": f"token {github_token}",
#             "Accept": "application/vnd.github.v3+json"
#         },
#         json={"source": {"branch": "main", "path": "/"}}
#     )
#     if pages_response.status_code not in [200, 201, 202]:
#         raise Exception(f"Failed to enable GitHub Pages: {pages_response.text}")

#     print("GitHub Pages enabled.")

#     # Construct the GitHub Pages URL
#     pages_url = f"https://{username}.github.io/{repo_name}/"

#     # Clean up the temporary directory
#     shutil.rmtree(temp_dir, ignore_errors=True)

#     time.sleep(25)

#     print(f"Your GitHub Pages site is live at: {pages_url}")
#     return pages_url
