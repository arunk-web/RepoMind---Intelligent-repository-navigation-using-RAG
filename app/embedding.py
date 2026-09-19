from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL_NAME

model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def generate_embedding(text):
    embedding = model.encode(text)
    return embedding


def generate_embedding_for_chunks(chunks):
    for chunk in chunks:
        chunk["embedding"] = model.encode(chunk["code"])
    return chunks
