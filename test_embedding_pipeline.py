from app.repo_clone import clone_repository
from app.chunk import extract_chunks_from_repo
from app.embedding import generate_embedding_for_chunks
from app.vector_store import store_chunks

# clone repo
path = clone_repository("https://github.com/arunk-web/RepoMind---Intelligent-repository-navigation-using-RAG", "storage/repos")
print("clone at: ", path)


# chunks
chunks = extract_chunks_from_repo(path)
print("total chunks:", len(chunks))


# embed
chunks_with_embedding = generate_embedding_for_chunks(chunks)

# verify
# print("first chunk name:",chunks_with_embedding[0]["name"])
# print("First chunk embedding shape:", len(chunks_with_embedding[0]["embedding"]))

store_chunks(chunks_with_embedding)
print("chunks stored")