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
import time
import math
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-embedding-001"
OUTPUT_DIM = 768
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}"
MAX_CHARS = 6000  # keep very long functions under the model's input limit


def _normalize(vec):
    # Gemini only returns pre-normalized vectors at 3072 dims, so normalize here
    norm = math.sqrt(sum(x * x for x in vec))
    return [x / norm for x in vec] if norm else vec


def _post(url, payload):
    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY is not set")

    headers = {"x-goog-api-key": GEMINI_API_KEY, "Content-Type": "application/json"}

    for attempt in range(4):
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        if response.status_code == 429:
            time.sleep(2 ** attempt)  # rate limited: wait and retry
            continue
        if not response.ok:
            raise Exception(f"Gemini embedding API error {response.status_code}: {response.text[:200]}")
        return response.json()

    raise Exception("Gemini embedding API rate limit hit, please try again in a minute")


def generate_embedding(text, task_type="RETRIEVAL_QUERY"):
    data = _post(
        f"{BASE_URL}:embedContent",
        {
            "content": {"parts": [{"text": text[:MAX_CHARS]}]},
            "taskType": task_type,
            "outputDimensionality": OUTPUT_DIM,
        },
    )
    return _normalize(data["embedding"]["values"])


def generate_embedding_for_chunks(chunks):
    batch_size = 100  # one API call per 100 chunks instead of one per chunk

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]

        batch_requests = [
            {
                "model": f"models/{MODEL}",
                "content": {"parts": [{"text": chunk["code"][:MAX_CHARS]}]},
                "taskType": "RETRIEVAL_DOCUMENT",
                "outputDimensionality": OUTPUT_DIM,
            }
            for chunk in batch
        ]

        data = _post(f"{BASE_URL}:batchEmbedContents", {"requests": batch_requests})

        for chunk, emb in zip(batch, data["embeddings"]):
            chunk["embedding"] = _normalize(emb["values"])

    return chunks
