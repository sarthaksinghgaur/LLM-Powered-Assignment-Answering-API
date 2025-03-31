import os, json
import feedparser
from reg_parserlib import extract_using_regex
import urllib.parse

def execute(question: str, parameter):
        #print(f"File Name: {os.path.basename(__file__)[0]}")
        
        topic, points = get_topic_points(question)
        latest_post_link = get_latest_post_link(topic, points)
        
        return latest_post_link
        
def get_latest_post_link(topic, min_points):
    topic = urllib.parse.quote(topic)
    # Define the HNRSS feed URL with the required parameters
    hnrss_url = f"https://hnrss.org/newest?q={topic}&points={min_points}"

    # Parse the RSS feed
    feed = feedparser.parse(hnrss_url)

    # Extract the link of the most relevant post
    if feed.entries:
        # Assuming the first entry is the most recent
        most_relevant_post_link = feed.entries[0].link
    else:
        most_relevant_post_link = "No post found with the given criteria."

    return most_relevant_post_link


def get_topic_points(text):
    regex_patterns = {
        "topic": {"pattern": r"Hacker News post mentioning ([\w\s]+) having at least (\d+) points?", "multiple": True}
    }
    reg_params = extract_using_regex(regex_patterns, text)
    topic = reg_params["topic"][-1][0] if "topic" in reg_params else "Indie+Hackers"
    points = int(reg_params["topic"][-1][1]) if "topic" in reg_params else 86

    return topic, points