# from sentence_transformers import SentenceTransformer
# from app.config import EMBEDDING_MODEL_NAME

# model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# def generate_embedding(text):
#     embedding = model.encode(text)
#     return embedding


# def generate_embedding_for_chunks(chunks):
#     for chunk in chunks:
#         chunk["embedding"] = model.encode(chunk["code"])
#     return chunks


import os
import requests
from dotenv import load_dotenv
 
load_dotenv()
 
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://router.huggingface.co/hf-inference/models/BAAI/bge-small-en-v1.5/pipeline/feature-extraction"
headers = { "Authorization":  f"Bearer {HF_TOKEN}"}
 
 
def generate_embedding(text):
    response = requests.post (
        API_URL,
        headers=headers,

        json={"inputs": text, "options": {"wait_for_model": True}}
    )
    result = response.json()
 
    if isinstance(result, dict) and "error" in result:

        raise Exception(f"HF Inference API error: {result['error']}")
 
    # API sometimes returns a nested list (token-level); if so, average it down to one vector
    if isinstance(result[0], list):

        num_tokens = len(result)

        dim = len(result[0])

        averaged = [sum(result[i][j] for i in range(num_tokens)) / num_tokens for j in range(dim)]
        return averaged
 
    return result
 
 
def generate_embedding_for_chunks(chunks):
    for chunk in chunks:

        chunk["embedding"] = generate_embedding(chunk["code"])
    return chunks
 
