# AI Engineering Intelligence Platform

An agentic codebase intelligence and code-graph search system designed for Python repositories. By combining Abstract Syntax Tree (AST) static analysis, Git history tracking, and vector semantic search, the platform builds a multi-dimensional knowledge graph of code architecture, call hierarchies, changesets, and issues. Users can query the repository through a multi-agent chat workflow orchestrated by LangGraph, featuring automated verification, reflection/retry loops, and LLM fallback logic.

---

## Tech Stack & Dependencies

- **Language:** Python 3.11.11 (specified in `runtime.txt`)
- **Web Framework:** FastAPI (ASGI server powered by Uvicorn)
- **Agentic Orchestration:** LangGraph (with custom state tracking and multi-turn loops)
- **Databases:**
  - **Neo4j:** Graph database storing syntax relationships, import structures, commit history, and issue connections.
  - **Pinecone:** Vector database for semantic similarity searches across chunked code files, commits, and pull requests.
  - **PostgreSQL:** Relational database storage (managed via SQLAlchemy ORM) for users, repository metadata, and conversation history.
- **LLM Providers:** Google Gemini SDK (`google-genai`) and Cohere SDK (`cohere`) with fallback failover.
- **Embeddings:** LangChain Cohere Embeddings (`embed-v4.0`)
- **Static Code Analysis:** Python AST (`ast` module) for syntax tree parsing.
- **Git Integration:** GitPython (`git`) for cloning and parsing repositories.
- **Authentication & Security:** JWT tokens (`python-jose`), password hashing (`passlib` with Argon2 context).

---

## Features

1. **Unified Code & Git Knowledge Graph (Neo4j)**
   - Extracts structural code relationships (`CONTAINS`, `DECLARES`, `CALLS`, `IMPORTS`, `DEPENDS_ON`).
   - Integrates Git history nodes (`Commit`, `Issue`) mapping which commits modified which files and which commits resolved specific issue numbers (`MODIFIES`, `FIXES`).

2. **Hybrid Retrieval (Vector + Graph)**
   - Combines semantic search via Pinecone (for code snippets, commits, and pull requests) with structural lookup via Neo4j (for call graph queries, callers, callees, and dependencies).

3. **Agentic Question-Answering (LangGraph Workflow)**
   - **Planner Node:** Evaluates the user's question and history to generate a structured execution plan.
   - **Executor Node:** Runs vector and graph query tools against the database registry.
   - **Verification Node:** Inspects query results. Decides to compile a final answer (`answer`), refine the plan and retry (`retry`), or stop due to missing evidence (`stop`).
   - **Reflection Node:** Tracks retry cycles (capped at 2 reflections) and feeds reasoning feedback back into the Planner.
   - **Report Node:** Formats proof and generates the final markdown report.

4. **Resilient LLM Failover**
   - Dual-provider support (Gemini & Cohere). Automatically routes requests to the secondary LLM if the primary provider hits quota constraints or rate limits.

5. **Multi-Tenant Ingestion Pipelines**
   - Validates target repository language (currently restricted to Python).
   - Asynchronously clones, chunks, embeds, parses, and structures repository records.
   - Implements transactional cleanups (rollback) across Pinecone, Neo4j, and local storage on ingestion failures.

---

## Project Structure

```text
├── .env.example                  # Template configuration for environment variables
├── .gitignore                    # Git ignore configurations (venv, data, caches)
├── requirements.txt              # Project package dependencies
├── runtime.txt                   # Specifies Python runtime version (python-3.11.11)
├── logs/                         # Execution tracing logs (workflows, nodes, timestamps)
├── data/                         # Local storage for cloned Git repositories
├── scripts/                      # Integration and module test scripts
└── app/                          # Core application package
    ├── main.py                   # FastAPI entrypoint and router registration
    ├── LangGraph/                # LangGraph state workflow configuration
    │   ├── workflow.py           # Compiles state graph and defines routing
    │   └── nodes/                # Node implementations (planner, executor, verifier, etc.)
    ├── agents/                   # Agent logic and prompt payloads
    │   ├── planner.py            # Planner agent
    │   ├── verifier.py           # Verification agent
    │   ├── report_generator.py   # Final reporter agent
    │   ├── router.py             # Conditional routing rules
    │   └── state.py              # Typed agent state schema
    ├── api/                      # FastAPI routing layer
    │   ├── dependencies/         # Security and database dependencies
    │   ├── routes/               # API endpoints (auth, chat, ingestion, repositories)
    │   └── schemas/              # Pydantic request/response models
    ├── auth/                     # JWT tokens, password hashing, and user DB access
    ├── conversation/             # Message and chat session DB access
    ├── core/                     # Configuration loading settings and logging
    ├── database/                 # SQLAlchemy connections and metadata base
    ├── git/                      # Git log history and issue number parse extraction
    ├── graph/                    # Neo4j connections, models, builders, and query layers
    ├── ingestion/                # Document loading, git cloning, AST parsing, and chunking
    ├── llm/                      # Gemini/Cohere SDK wrappers and LLM fallback router
    ├── parsing/                  # Rich Python AST extractors and symbol table builders
    ├── repository/               # Repository DB mappings and services
    ├── retrieval/                # Pinecone retriever interface
    ├── services/                 # Embeddings generation, Pinecone upsert, and cleanups
    ├── tools/                    # Tool execution registry (GraphTool, VectorTool)
    ├── tracing/                  # Trace logger capturing execution logs
    └── utils/                    # GitHub metadata verification helpers
```

---

## Environment Variables

Create a `.env` file in the root directory. Below are the required environment variable names (do not expose actual secret values in production configurations):

```env
# Application Settings
APP_NAME="Engineering Intelligence Platform"
APP_VERSION="1.0.0"
HOST="127.0.0.1"
PORT=8000
DEBUG=True

# Neo4j Database Configuration
NEO4J_URI=
NEO4J_USERNAME=
NEO4J_PASSWORD=

# Vector Split Configurations
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Pinecone Vector Database Configuration
PINECONE_API_KEY=
PINECONE_INDEX_NAME=

# LLM Providers Keys & Models Configuration
GEMINI_API_KEY=
COHERE_API_KEY=
GEMINI_MODEL=
COHERE_MODEL=
COHERE_EMBEDDING_MODEL=
LLM_PROVIDER=

# Authentication Configs
JWT_SECRET=

# Relational Database URL (e.g. PostgreSQL)
DATABASE_URL=
```

---

### Start the FastAPI Server

To start the API in hot-reload development mode:

```bash
python -m uvicorn app.main:app --reload
```

The server will start on `http://127.0.0.1:8000`. You can access the auto-generated API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.


---

