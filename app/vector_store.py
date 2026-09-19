import chromadb , uuid
from app.config import VECTOR_DB_PATH,COLLECTION_NAME
# chroma connection
client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

collection = client.get_or_create_collection(name=COLLECTION_NAME)

def store_chunks(chunks):
    ids = []
    embeddings = []
    metadatas = []
    documents = []

    for i ,chunk in enumerate(chunks):
        # ids.append(uuid.uuid4())   method to generate a unique id
        ids.append(str(i))
        embeddings.append(chunk["embedding"].tolist())
        metadatas.append({
            "name" : chunk["name"],
            "file" : chunk["file"],
            "start_line" : chunk["start_line"],
            "end_line" : chunk["end_line"]
        })
        documents.append(chunk["code"])

    collection.add(
        ids = ids,
        embeddings = embeddings,
        metadatas = metadatas,
        documents = documents
    )