from sentence_transformers import SentenceTransformer


model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def generate_embedding_for_chunks(chunks):
    for chunk in chunks:
        chunk["embedding"] = model.encode(chunk["code"])
    return chunks
    