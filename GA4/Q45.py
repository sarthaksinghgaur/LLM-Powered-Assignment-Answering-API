import os, json, requests, time

from reg_parserlib import extract_using_regex

def execute(question: str, parameter):
        print(f"File Name: {os.path.basename(__file__)[0]}")
        
        city, country = get_city_country_name(question)
        max_latitude = get_max_latitude_nominatim(city, country)
        return max_latitude
        
def get_max_latitude_nominatim(city, country):
    """Fetch the maximum latitude of a city's bounding box using Nominatim API."""
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': f'{city}, {country}', 'format': 'json', 'limit': 1}
    headers = {'User-Agent': 'UrbanRideApp/1.0 (contact@urbanride.com)'}  # Update with a real email

    for attempt in range(3):  # Retry up to 3 times if blocked
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 403:
            print("❌ Access forbidden. Retrying in 10 seconds...")
            time.sleep(10)
            continue  # Retry

        response.raise_for_status()  # Raise an error for other HTTP issues
        data = response.json()

        if data:
            bounding_box = data[0]['boundingbox']
            return max(float(bounding_box[0]), float(bounding_box[1]))  # Max latitude

    print("⚠ Nominatim API blocked. Switching to OpenCage API...")
    return get_max_latitude_opencage(city, country)  # Use alternative API

def get_max_latitude_opencage(city, country):
    """Fetch the maximum latitude using OpenCage API."""
    API_KEY = 'YOUR_OPENCAGE_API_KEY'  # Get a free API key from https://opencagedata.com
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {'q': f'{city}, {country}', 'key': API_KEY}

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    if not data['results']:
        raise ValueError(f"🚨 No data found for {city}, {country}")

    bounds = data['results'][0]['bounds']
    return max(bounds['northeast']['lat'], bounds['southwest']['lat'])
        
def get_city_country_name(text):
    regex_patterns = {
        "city": {"pattern": r'city ([\w\s]+) in the country ([\w\s]+) on the Nominatim API', "multiple": True}
    }
    reg_params = extract_using_regex(regex_patterns, text)
    city = reg_params["city"][-1][0] if "city" in reg_params else "Chennai"
    country = reg_params["city"][-1][1] if "city" in reg_params else "India"
    
    return city, country