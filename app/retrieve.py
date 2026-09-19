from app.vector_store import collection
from app.embedding import generate_embedding

def retrieve_chunks(question):
    user_query_embeddings = generate_embedding(question)
    result = collection.query(
        query_embeddings = [user_query_embeddings],
        n_results = 3
    )

    return result