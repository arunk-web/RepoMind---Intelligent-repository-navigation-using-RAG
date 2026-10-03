from app.bm25_search import search_bm25
from app.embedding import generate_embedding
from app.vector_store import collection

def retrieve_chunks(question):
    user_query_embeddings = generate_embedding(question)
    semantic_result = collection.query(
        query_embeddings=[user_query_embeddings],
        n_results=3
    )
    
    bm25_result = search_bm25(question, top_n=3)
    
    bm25_documents = []
    bm25_metadatas = []
    
    for c in bm25_result:
        bm25_documents.append(c["code"])
        bm25_metadatas.append({
            "name": c["name"],
            "file": c.get("file", ""),
            "start_line": c.get("start_line", 0),
            "end_line": c.get("end_line", 0)
        })
    
    combined_documents = semantic_result["documents"][0] + bm25_documents
    combined_metadatas = semantic_result["metadatas"][0] + bm25_metadatas
    
    return {"documents": [combined_documents], "metadatas": [combined_metadatas]}