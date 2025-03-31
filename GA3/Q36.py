import os, json

def execute(question: str, parameter):
    json_payload = detect_and_generate_code(question)
    return json_payload

def detect_and_generate_code(question):
    """
    Detects whether the given question is asking for cosine similarity calculation
    between text embeddings and returns the appropriate Python function.
    """
    # Keywords to check if the question is relevant
    keywords = [
        "ShopSmart", "customer feedback", "text embeddings", "cosine similarity",
        "most similar", "pair", "array of floats"
    ]

    # Check if all required keywords are in the question
    if all(keyword.lower() in question.lower() for keyword in keywords):
        # If the question matches, return the required function
        return """import numpy as np

def most_similar(embeddings):
    max_similarity = -1
    most_similar_pair = None

    phrases = list(embeddings.keys())

    for i in range(len(phrases)):
        for j in range(i + 1, len(phrases)):
            v1 = np.array(embeddings[phrases[i]])
            v2 = np.array(embeddings[phrases[j]])

            similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_pair = (phrases[i], phrases[j])

    return most_similar_pair
"""