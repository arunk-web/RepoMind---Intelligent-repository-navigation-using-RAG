# RepoMind — AI-Powered Codebase Q&A Assistant

RepoMind lets you point at any public GitHub repository and ask questions about it in plain English. It clones the repo, breaks the Python code down into functions and class methods using AST-based parsing, embeds each chunk, stores them in a vector database, and answers your questions using a RAG (Retrieval-Augmented Generation) pipeline — with real code as context.

Unlike simple PDF/document RAG tools, RepoMind understands **code structure**. Chunks are never split mid-function — every chunk is a complete function or method, so retrieved context is always coherent.

The system's reliability isn't just assumed — it's measured. Evaluated with the [RAGAS](https://github.com/explodinggradients/ragas) framework on a custom benchmark, RepoMind achieves **91–98% faithfulness** and **~88% answer relevancy**, with **~1.45s average end-to-end response time** (near-instant on repeated queries, thanks to caching).

---

## How It Works

```mermaid
flowchart TD
    A[GitHub Repo URL] --> B[Clone Repository]
    B --> C[Walk repo files with os.walk]
    C --> D[Parse each .py file with AST]
    D --> E[Extract functions & class methods as chunks]
    E --> F[Generate embeddings - HuggingFace model]
    F --> G[Store chunks + embeddings in ChromaDB]

    H[User Question] --> I[Generate question embedding]
    I --> J[Retrieve top-k similar chunks from ChromaDB]
    J --> K[Build context from retrieved chunks]
    K --> L[Send question + context to LLM - Groq]
    L --> M[Return natural language answer]

    G -.stored vectors.-> J
```

**Indexing pipeline** (`POST /index`): Clone → Chunk (AST) → Embed → Store
**Query pipeline** (`POST /ask`): Embed question → Retrieve similar chunks → Generate answer with LLM

---

## Features

- 🔍 **AST-based code chunking** — splits code at function/class-method boundaries, never mid-function
- 🧠 **Semantic search** — finds relevant code by meaning, not just keyword matching
- 💬 **Natural language Q&A** — ask questions like "how does authentication work?" and get a real answer with code references
- 📁 **Recursive repo scanning** — automatically finds and processes every `.py` file in a cloned repository
- ⚡ **Free & open embedding/LLM stack** — HuggingFace embeddings (local, no cost) + Groq LLM (free tier, fast inference)
- 🧩 **Clean modular architecture** — each pipeline stage (`clone`, `chunk`, `embed`, `store`, `retrieve`, `llm`) lives in its own file
- 📎 **Source-attributed answers** — every response includes the exact file path, function/method name, and line numbers it was drawn from
- 🚀 **In-memory query caching** — repeated questions are served from cache, cutting response time from ~2.9s to <1ms
- 📊 **Measured, not assumed** — evaluated with RAGAS on a custom benchmark; see [Evaluation & Performance](#evaluation--performance)

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI + Uvicorn |
| Repo Cloning | GitPython |
| Code Parsing | Python `ast` module |
| Embeddings | Sentence-Transformers (`BAAI/bge-small-en-v1.5`) |
| Vector Database | ChromaDB (persistent, local) |
| LLM | Groq API |
| Config | python-dotenv |

---

## Project Structure

```
RepoMind/
├── app/
│   ├── main.py           # FastAPI app + endpoints (/index, /ask)
│   ├── config.py         # Centralized config (paths, model names)
│   ├── schemas.py        # Pydantic request models
│   ├── repo_clone.py     # Clones a GitHub repo into a unique local folder
│   ├── chunk.py          # AST-based function/class-method chunking
│   ├── embedding.py      # Generates embeddings for text/chunks
│   ├── vector_store.py   # ChromaDB client + storage logic
│   ├── retrieve.py       # Semantic retrieval from ChromaDB
│   └── llm.py            # Groq LLM call for answer generation
├── storage/
│   ├── repos/             # Cloned repositories (gitignored)
│   └── vector_db/         # ChromaDB persistent storage (gitignored)
├── requirements.txt
├── .env                   # API keys (gitignored)
└── .gitignore
```

---

## Setup

### 1. Clone this repository

```bash
git clone https://github.com/arunk-web/RepoMind---Intelligent-repository-navigation-using-RAG.git
cd RepoMind
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

macOS / Linux:
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com).

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be running at `http://127.0.0.1:8000`. Interactive docs (Swagger UI) are available at `http://127.0.0.1:8000/docs`.

---

## API Usage

### Index a repository

```http
POST /index
Content-Type: application/json

{
  "repo_url": "https://github.com/some-user/some-python-repo"
}
```

**Response:**
```json
{
  "message": "repo indexed successfully",
  "total chunks": 42
}
```

### Ask a question

```http
POST /ask
Content-Type: application/json

{
  "question": "How does the path generation work?"
}
```

**Response:**
```json
{
  "answer": "The path-generation logic lives in the generate_unique_path function...",
  "sources": [
    {"file": "app/repo_clone.py", "name": "generate_unique_path", "start_line": 10, "end_line": 13},
    {"file": "app/repo_clone.py", "name": "clone_repository", "start_line": 16, "end_line": 19}
  ]
}
```

Every answer is grounded in real code — `sources` tells you exactly which file, function, and line range it came from, so you can jump straight to the source and verify it yourself.

Repeated questions are served from an in-memory cache, so the same question asked twice returns near-instantly on the second call.

---

## How Chunking Works

Most RAG tools split text into fixed-size chunks (e.g. every 500 characters), which is fine for prose but breaks code — a function can get cut in half, destroying its context.

RepoMind instead parses each Python file into an **Abstract Syntax Tree (AST)** and walks it in two passes:

1. **Top-level functions** — extracted as standalone chunks
2. **Classes** — for each class, its methods are extracted as separate chunks, named `ClassName.method_name` so their origin is never ambiguous

This guarantees every chunk is a complete, syntactically valid unit of code, which significantly improves retrieval quality.

---

## Evaluation & Performance

Rather than assuming the RAG pipeline works well, it was benchmarked using [RAGAS](https://github.com/explodinggradients/ragas) on a custom 5-question dataset built against this repository's own codebase, with Groq as the judge LLM and the same HuggingFace embedding model used in production.

| Metric | Score |
|---|---|
| Faithfulness | 91–98% |
| Answer Relevancy | ~88% |

**Faithfulness** measures how well the generated answer is grounded in the retrieved code context (i.e. how little the LLM "makes up"). **Answer Relevancy** measures how directly the answer addresses the question asked.

### Latency Breakdown

| Stage | Avg. Time |
|---|---|
| Retrieval (ChromaDB) | ~70ms |
| LLM Generation (Groq) | ~1.4–2.9s |
| **End-to-end (cache miss)** | **~1.45–2.9s** |
| **End-to-end (cache hit)** | **<1ms** |

Retrieval is a small fraction of total latency — LLM generation is the dominant cost, which is expected given the sequential nature of token generation. Query-level caching eliminates this cost entirely for repeated questions, cutting response time by **over 99.99%** on cache hits.

`eval.py` in the repo runs this benchmark end-to-end and can be re-run against any indexed repository.

---

## Roadmap / Future Improvements

- [ ] Multi-repository support (isolated vector namespaces per repo)
- [ ] Multi-language support via `tree-sitter` (JavaScript, TypeScript, etc.)
- [ ] Hybrid retrieval (BM25 keyword search + semantic search)
- [ ] Chunking strategy comparison (AST-based vs. naive fixed-size splitting)
- [ ] React-based chat frontend

---

## Why This Project

Codebase onboarding is slow — new contributors and engineers often spend hours grepping through unfamiliar code or waiting on senior developers to explain how things work. RepoMind is a simplified, self-built version of the "codebase-aware assistant" pattern used by tools like Cursor and GitHub Copilot Chat, built from scratch to understand how AST-based chunking, embeddings, vector search, and RAG pipelines actually work under the hood.

---

## License

MIT
