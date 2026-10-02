from app.bm25_search import build_bm25_index, search_bm25

sample_chunks = [
    {"name": "add", "code": "def add(a, b): return a + b"},
    {"name": "clone_repository", "code": "def clone_repository(url, mainpath): git.Repo.clone_from(url, final_path)"},
    {"name": "generate_unique_path", "code": "def generate_unique_path(mainpath): unique_id = str(uuid.uuid4())"},
]

build_bm25_index(sample_chunks)
results = search_bm25("how does clone_repository work")

for r in results:
    print(r["name"])