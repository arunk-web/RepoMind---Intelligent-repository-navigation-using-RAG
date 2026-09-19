# RepoMind — AI-Powered Codebase Q&A Assistant

RepoMind lets you point at any public GitHub repository and ask questions about it in plain English. It clones the repo, breaks the Python code down into functions and class methods using AST-based parsing, embeds each chunk, stores them in a vector database, and answers your questions using a RAG (Retrieval-Augmented Generation) pipeline — with real code as context.

Unlike simple PDF/document RAG tools, RepoMind understands **code structure**. Chunks are never split mid-function — every chunk is a complete function or method, so retrieved context is always coherent.

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
  "answer": "The path-generation logic lives in the generate_unique_path function..."
}
```

---

## How Chunking Works

Most RAG tools split text into fixed-size chunks (e.g. every 500 characters), which is fine for prose but breaks code — a function can get cut in half, destroying its context.

RepoMind instead parses each Python file into an **Abstract Syntax Tree (AST)** and walks it in two passes:

1. **Top-level functions** — extracted as standalone chunks
2. **Classes** — for each class, its methods are extracted as separate chunks, named `ClassName.method_name` so their origin is never ambiguous

This guarantees every chunk is a complete, syntactically valid unit of code, which significantly improves retrieval quality.

---

## Roadmap / Future Improvements

- [ ] Multi-repository support (isolated vector namespaces per repo)
- [ ] Multi-language support via `tree-sitter` (JavaScript, TypeScript, etc.)
- [ ] Retrieval evaluation with RAGAS (faithfulness, context precision/recall benchmarks)
- [ ] Response caching for repeated/similar queries
- [ ] Source citation with clickable file + line references
- [ ] React-based chat frontend

---

## Why This Project

Codebase onboarding is slow — new contributors and engineers often spend hours grepping through unfamiliar code or waiting on senior developers to explain how things work. RepoMind is a simplified, self-built version of the "codebase-aware assistant" pattern used by tools like Cursor and GitHub Copilot Chat, built from scratch to understand how AST-based chunking, embeddings, vector search, and RAG pipelines actually work under the hood.

---

## License

MIT