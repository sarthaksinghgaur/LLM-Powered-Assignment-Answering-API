import os, json, re

def execute(question: str, parameter):
    timestamp, useful_stars = parameter["filter_date_iso"], get_usefulstars(question)
    
    return generate_duckdb_query(timestamp, useful_stars)
        
def generate_duckdb_query(timestamp, useful_stars):
    # Constructing the SQL query using the extracted values
    query = f"""
    SELECT post_id
    FROM (
        SELECT post_id
        FROM (
            SELECT post_id,
                    json_extract(comments, '$[*].stars.useful') AS useful_stars
            FROM social_media
            WHERE timestamp >= '{timestamp}'
        )
        WHERE EXISTS (
            SELECT 1 FROM UNNEST(useful_stars) AS t(value)
            WHERE CAST(value AS INTEGER) >= {useful_stars}
        )
    )
    ORDER BY post_id;
    """
    cleaned_answer = query.replace("\n", " ").strip()
    return cleaned_answer
    

def get_usefulstars(question):
    matches = re.findall(r"with (\d+) useful stars", question)
    return int(matches[-1]) if matches else None