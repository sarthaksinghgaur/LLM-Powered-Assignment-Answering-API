import os, json, requests, re, parse
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from urllib.parse import quote
from bs4 import BeautifulSoup
from request_context import current_request_var

def execute(question: str, parameter):
    #print(f"File Name: {os.path.basename(__file__)[0]}")
    request = request = current_request_var.get()
    base_url = str(request.base_url)
    # Check if the request is behind a proxy and use "https" if needed
    if request.headers.get("X-Forwarded-Proto") == "https":
        base_url = base_url.replace("http://", "https://")

    # Ensure base_url always ends with "/"
    if not base_url.endswith("/"):
        base_url += "/"
        
    return base_url + "wikiheaders"
        
def get_country_outline(country: str):
    if not country:
        raise HTTPException(status_code=400, detail="Country parameter is required")

    url = get_wikipedia_url(country)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=404, detail=f"Error fetching Wikipedia page: {e}")

    headings = extract_headings_from_html(response.text)
    if not headings:
        raise HTTPException(status_code=404, detail="No headings found in the Wikipedia page")

    markdown_outline = generate_markdown_outline(headings)
    return JSONResponse(content={"outline": markdown_outline})
        
def get_wikipedia_url(country: str) -> str:
    return f"https://en.wikipedia.org/wiki/{quote(country.strip().replace(' ', '_'))}"
        
def extract_headings_from_html(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.find("div", class_="mw-page-container")
    headings = []
    for level in range(1, 7):
        for tag in content_div.find_all(f'h{level}'):
            headings.append((level, tag.get_text(strip=True)))
    return headings

def generate_markdown_outline(headings: list) -> str:
    markdown_outline = "## Contents\\n\\n"
    for level, heading in headings:
        markdown_outline += "#" * level + f" {heading}\\n\\n"
    return markdown_outline