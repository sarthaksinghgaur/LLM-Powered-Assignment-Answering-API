import os, json, requests, re, parse

from bs4 import BeautifulSoup

regex_patterns = {
    "filter": {"pattern": r"between (\d+) and (\d+)", "multiple": True},
    "titles": r"first (\d+) titles"
}

def execute(question: str, parameter):
    print(f"File Name: {os.path.basename(__file__)[0]}")
    parameters = find_filter_format(question)
    result = None
    if parameters and "filter" in parameters and "titles" in parameters:
        if type(parameters["filter"]) == list:
            result = fetch_filtered_imdb_titles(int(parameters["filter"][0][0]), int(parameters["filter"][0][1]), int(parameters["titles"]))
        else:
            result = fetch_filtered_imdb_titles(int(parameters["filter"][0]), int(parameters["filter"][1]), int(parameters["titles"]))
    else:
        result = fetch_filtered_imdb_titles()
        
    return result

def fetch_filtered_imdb_titles(min_rating=3.0, max_rating=7.0, number_of_titles=25):
    # IMDb search URL without title_type filter
    url = f"https://www.imdb.com/search/title/?user_rating={min_rating},{max_rating}"
    headers = {
        "User-Agent": "Mozilla/5.0"

    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch page:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    movies = []

    # Select up to 25 movie items
    movie_items = soup.select('.ipc-metadata-list-summary-item')[:number_of_titles]

    for item in movie_items:
        title_element = item.select_one('.ipc-title__text')
        year_element = item.select_one('.dli-title-metadata-item')
        rating_element = item.select_one('.ipc-rating-star--rating')

        if title_element and year_element:
            # Extract ID
            link_tag = item.select_one('a[href*="/title/tt"]')
            match = re.search(r'tt\d+', link_tag['href']) if link_tag else None
            imdb_id = match.group(0) if match else None

            # Extract and clean fields
            title = title_element.get_text(strip=True)
            year = year_element.get_text().replace('\xa0', ' ')  # Preserve NBSP
            rating = rating_element.get_text(strip=True) if rating_element else None

            try:
                rating_float = float(rating)
                if min_rating <= rating_float <= max_rating:
                    movies.append({
                        "id": imdb_id,
                        "title": title,
                        "year": year,
                        "rating": rating
                    })
            except (ValueError, TypeError):
                continue
    
    return movies
    #return json.dumps(movies, indent=2, ensure_ascii=False)
        
def find_filter_format(question):
    regex_params = extract_using_regex(question)
    print(regex_params)
    return regex_params
    
def extract_using_regex(text):
    extracted = {}
    for param, pattern in regex_patterns.items():
        if isinstance(pattern, str):
            matches = re.search(pattern, text)
            if matches:
                extracted[param] = matches.groups()[0] if matches.groups() else matches.group()
        elif "multiple" in pattern and pattern["multiple"]:
            matches = re.findall(pattern["pattern"], text)  # Finds all occurrences
            if matches:
                extracted[param] = matches
        elif pattern["group"]:
            matches = re.search(pattern["pattern"], text)
            if matches:
                extracted[param] = matches.group()
    return extracted