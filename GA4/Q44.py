import os, json, requests, httpx

from reg_parserlib import extract_using_regex

API_KEY = "d508f0f12d23e6fabf5fb00f94ee5713"
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

def execute(question: str, parameter):
    #print(f"File Name: {os.path.basename(__file__)[0]}")
    
    city_name = get_city_name(question)
    forecast = get_weather_forecast_api(city_name)
    
    return forecast

def get_weather_forecast_api(city):
    api = "https://locator-service.api.bbci.co.uk/locations"
    params = {
        "api_key": "AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv",
        "stack": "aws",
        "locale": "en",
        "filter": "international",
        "place-types": "settlement,airport,district",
        "order": "importance",
        "s": city,
        "a": "true",
        "format": "json"
    }

    response = httpx.get(api, params=params)

    if response.status_code == 200:
        data = response.json()
        id = data["response"]["results"]["results"][0]["id"]
        print(data["response"]["results"]["results"][0]["id"])
        api= f"https://weather-broker-cdn.api.bbci.co.uk/en/forecast/aggregated/{id}"
        response = httpx.get(api)
        if response.status_code == 200:
            weather_data = response.json()
            forecasts = weather_data["forecasts"]
            result = {forecast["summary"]["report"]["localDate"] : forecast["summary"]["report"]["enhancedWeatherDescription"] for forecast in forecasts}
            return result
    else:
        print(f"Error {response.status_code}: {response.text}")
        
def get_weather_forecast(city):
    """Fetches 5-day weather forecast for the given city."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",  # Temperature in Celsius
    }

    response = requests.get(BASE_URL, params = params)

    if response.status_code != 200:
        print(f"Error fetching weather data: {response.json()}")
        return None

    data = response.json()

    weather_forecast = {}
    for entry in data["list"]:
        date = entry["dt_txt"].split(" ")[0]  # Extract YYYY-MM-DD
        description = entry["weather"][0]["description"]

        if date not in weather_forecast:
            weather_forecast[date] = description

    return weather_forecast

def get_city_name(text):
    regex_patterns = {
        "city": {"pattern": r"for (\w+)\?", "multiple": True}
    }
    reg_params = extract_using_regex(regex_patterns, text)
    if "city" in reg_params:
        return reg_params["city"][-1]
    else:
        return "Chennai"