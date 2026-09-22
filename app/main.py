from fastapi import FastAPI , HTTPException
from app.schemas import IndexRequest , AskRequest
from app.chunk import extract_chunks_from_repo
from app.embedding import generate_embedding_for_chunks
from app.llm import get_answer_from_llm
from app.repo_clone import clone_repository
from app.retrieve import retrieve_chunks
from app.vector_store import store_chunks
from app.config import REPO_STORAGE_PATH
import time

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


# @app.get('/')
# def hello():
#     return {'message':'hello'}

# path = clone_repository("https://github.com/arunk-web/AskPDF", "storage/repos")
# print(path)

@app.post("/index")
def index_repo(request : IndexRequest):
    try:
        path = clone_repository(request.repo_url,REPO_STORAGE_PATH)
        chunks = extract_chunks_from_repo(path)
        chunks_with_embedding = generate_embedding_for_chunks(chunks)
        store_chunks(chunks_with_embedding)
        return {"message": "repo indexed successfully" ,"total chunks": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=400 , detail=f"Failed to load index repo: {str(e)}")

cache = {}

@app.post("/ask")
def user_question(request : AskRequest):
    start = time.time()
    try:
        query = request.question
        if query in cache:
            end = time.time()
            print(f"cache hit time:{end-start:.4f}s")
            return cache[query]
        else:
            user_query_chunk = retrieve_chunks(query)
            sources = user_query_chunk["metadatas"][0]
            context= "\n\n".join(user_query_chunk["documents"][0])
            answer = get_answer_from_llm(query,context)
            cache[query] = {
                "answer" :answer,
                "sources" : sources
            }
            
            end = time.time()
            print(f"cache miss: {end-start:.4f}s")
        return cache[query]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed to give answer: {str(e)}")

