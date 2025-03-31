import os, json, io, re
import pandas as pd
from fuzzywuzzy import fuzz, process

def execute(question: str, parameter, file_bytes):
    file_io = io.BytesIO(file_bytes)
    product_name, min_units, target_city = get_parameters(question)
    city_sales = analyze_sales(file_io, product_name, min_units, target_city)
    #city_sales = analyze_sales_fuzzy(file_io, product_name, min_units, target_city)
    return int(city_sales)
    

def analyze_sales(file_io, product_name, min_units, target_city):
    df = pd.read_json(file_io)
    df['city'] = cluster_cities(df['city'], [target_city])        
    
    df_filtered = df[(df['product'] == product_name) & (df['sales'] >= min_units)]

    # Aggregate sales by city
    df_grouped = df_filtered.groupby("city")["sales"].sum().reset_index()

    # # Identify the top-performing city
    # top_city = df_grouped.sort_values(by="sales", ascending=False).iloc[0]

    # Find sales for Jakarta
    city_sales = df_grouped[df_grouped["city"].str.lower() == str(target_city).lower()]["sales"].sum()
    return city_sales

def analyze_sales_fuzzy(file_io, product_name, min_units, target_city):
    # Extract food item, city, and sales threshold dynamically from the question
    data = pd.read_json(file_io)

    # Group city names using phonetic clustering
    city_to_cluster = phonetic_cluster(data['city'])

    # Filter entries for the specified food item and sales >= min_sales
    filtered_data = data[(data['product'] == product_name) & (data['sales'] >= min_units)]

    # Apply the clustering to city names (use .loc to avoid the warning)
    filtered_data.loc[:, 'clustered_city'] = filtered_data['city'].apply(lambda x: city_to_cluster.get(x, x))

    # Aggregate sales by city (clustered)
    aggregated_sales = filtered_data.groupby('clustered_city')['sales'].sum().reset_index()

    #print(aggregated_sales)
    # Check for sales in the specified city
    city_sales = aggregated_sales[aggregated_sales['clustered_city'].str.contains(target_city, case=False, na=False)]

    # Return the result for the specified city and food item
    return int(city_sales['sales'].sum()) if not city_sales.empty else 0

def cluster_cities(city_series, known_cities):
    """Standardize city names using fuzzy matching."""
    city_series = city_series.fillna('Unknown')

    def get_closest_city(city_name):
        best_match = process.extractOne(city_name, known_cities, scorer=fuzz.token_set_ratio)
        if best_match and best_match[1] > 80:  # Adjust the threshold as needed
            return best_match[0]
        return city_name

    city_series = city_series.apply(get_closest_city)
    return city_series

def phonetic_cluster(cities):
    clusters = {}
    #print(cities)
    for city in cities:
        found_cluster = False
        for cluster_city in clusters:
            if fuzz.ratio(city.lower(), cluster_city.lower()) > 80:  # Threshold for similarity
                clusters[cluster_city].append(city)
                found_cluster = True
                break
        if not found_cluster:
            clusters[city] = [city]

    city_to_cluster = {}
    for cluster_city, city_list in clusters.items():
        for city in city_list:
            city_to_cluster[city] = cluster_city

    return city_to_cluster

def get_parameters(question):
    # How many units of Gloves were sold in Guangzhou on transactions with at least 7 units?
    # Extract product (assuming it's a single word capitalized)
    product_match = re.findall(r"units of (\w+)", question)

    # Extract city (assuming it's a capitalized word after "in")
    city_match = re.findall(r"sold in (\w+)", question)

    # Extract units (assuming it's a number after "at least")
    units_match = re.findall(r"at least (\d+) units?", question)

    # Take the last occurrence if multiple matches exist
    product = product_match[-1] if product_match else None
    city = city_match[-1] if city_match else None
    units = int(units_match[-1]) if units_match else None
    
    return (product, units, city)