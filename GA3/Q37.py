import os, json, numpy as np, httpx
from request_context import current_request_var

api_key = "Io4hBJXa8XEOT6cUwFHa2RcPhVLjCF8zfQBLTl3e_q2XJlI10N-P_m72gA" 

def execute(question: str, parameter):
    request = current_request_var.get()
    base_url = str(request.base_url)

    # Check if the request is behind a proxy and use "https" if needed
    if request.headers.get("X-Forwarded-Proto") == "https":
        base_url = base_url.replace("http://", "https://")

    # Ensure base_url always ends with "/"
    if not base_url.endswith("/"):
        base_url += "/"
        
    return base_url + "similarity"

def get_similarity(docs, query):
    doc_embeddings = [get_embedding(doc) for doc in docs]
    query_embedding = get_embedding(query)

    similarities = [cosine_similarity(query_embedding, doc_emb) for doc_emb in doc_embeddings]
    ranked_docs = [doc for _, doc in sorted(zip(similarities, docs), reverse=True)]

    return {"matches": ranked_docs[:3]}

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# # Function to generate embeddings
# def get_embedding(text):
#     response = client.embeddings.create(
#         model="text-embedding-3-small",
#         input=text
#     )
#     return response.data[0].embedding  # Extract the embedding

def get_embedding(user_input: str):
    response = httpx.post(
        "https://api.openai.com/v1/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "text-embedding-3-small",
            "input": user_input,
        },
    )
    return response.json()["data"][0]["embedding"]