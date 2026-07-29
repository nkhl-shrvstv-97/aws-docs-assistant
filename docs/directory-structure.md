# Directory Structure and Application Layout

This document details the folder hierarchy of the application backend, testing setup, and ingestion tools.

---

## 1. Project Directory Layout

```text
aws-docs-assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entrypoint & static mounting
│   │   ├── config.py               # Environment configuration & settings
│   │   ├── static/                 # Embedded Frontend UI assets
│   │   │   └── index.html          # Simple Web Chat interface
│   │   ├── agents/                 # LangGraph Agent logic
│   │   │   ├── __init__.py
│   │   │   ├── state.py            # LangGraph state schema
│   │   │   ├── graph.py            # Graph assembly & compilation
│   │   │   ├── nodes/              # Node definitions
│   │   │   │   ├── classify.py     # Domain classification
│   │   │   │   ├── rewrite.py      # Query translation
│   │   │   │   ├── retrieve.py     # Local VDB query node
│   │   │   │   ├── grade.py        # Doc grader & generation grader
│   │   │   │   ├── search.py       # Live AWS Doc search node
│   │   │   │   └── generate.py     # Final response generation
│   │   │   └── prompts.py          # Bedrock prompt templates
│   │   ├── db/                     # Vector DB client & connections
│   │   │   ├── __init__.py
│   │   │   ├── session.py          # SQLAlchemy engine & sessionmaker
│   │   │   └── models.py           # DB models (DocumentChunks schema)
│   │   └── tools/                  # Retriever & live search tools
│   │       ├── __init__.py
│   │       ├── vector_store.py     # pgvector client operations
│   │       └── doc_search.py       # Scraper/Search engine client for AWS Docs
│   ├── ingestion/                  # Doc ingestion & embedding pipeline
│   │   ├── ingest.py               # Main ingestion runner
│   │   ├── parser.py               # HTML/Markdown parser
│   │   └── data/                   # Seed files for local indexing
│   ├── tests/                      # Unit & integration tests
│   ├── Dockerfile
│   └── requirements.txt
├── terraform/                      # Infrastructure as Code
│   ├── main.tf                     # Entry point for resources
│   ├── variables.tf                # Configuration variables
│   ├── outputs.tf                  # Infrastructure output exports
│   ├── vpc.tf                      # Network setup
│   ├── rds.tf                      # RDS PostgreSQL with pgvector
│   └── apprunner.tf                # App Runner serverless configs
├── cli.py                          # Local CLI client for terminal-based chat
├── problem-statement.md
└── README.md
```

---

## 2. Component Explanations

### Backend App (`backend/app/`)
* **`main.py`:** Initiates FastAPI, configures CORS middleware, mounts endpoints (`/chat`, `/end-session`), and sets up lifespans (pre-compiling the LangGraph workflow).
* **`config.py`:** Reads environment configurations using Pydantic Settings (e.g. AWS Bedrock region, database connection string, API keys, etc.).
* **`agents/`:** Encapsulates the entire decision-making loop. Standardizes state schemas, nodes (tasks), router transitions, and template configurations.
* **`db/`:** Standard SQLAlchemy session management. Models map directly to the PostgreSQL database schemas (both vector and relational tables).
* **`tools/`:** Reusable tool modules. Contains queries targeting the PostgreSQL database using pgvector helper functions, and web search wrappers.

### Ingestion Suite (`backend/ingestion/`)
* **`ingest.py`:** A runnable script that accepts files or directories, parses them, interacts with Bedrock Embeddings, and inserts them into PostgreSQL. Used for indexing initial doc segments during local development.
* **`parser.py`:** Parses HTML raw content using BeautifulSoup4 to yield metadata payloads and text strings.
* **`data/`:** Directory holding local Markdown/HTML files containing AWS doc sample subsets for embedding seeding.

### Tests Suite (`backend/tests/`)
* Contains unit tests focusing on parser operations, rewriter functions, vector searches, and API mock-ups for Bedrock models using `pytest` and stub/mock utilities.

---

## 3. UI & CLI Client Implementation Checklist

Use this checklist to write and test the interactive interface methods for the assistant:

### Phase 1: Local Terminal Client (`cli.py`)
- [ ] Create `cli.py` in the root workspace directory.
- [ ] Implement query loop importing `requests` to prompt input continuously.
- [ ] Add session tracking by dynamically generating a new UUID (`thread_id`) at client startup.
- [ ] Add exit command handling:
  - [ ] Intercept commands like "exit" or "quit".
  - [ ] Make a POST query to backend `/end-session` with the current `thread_id` to trigger long term summarization.
  - [ ] Exit execution.
- [ ] Write logic to print returned `generation` output, along with index items within `citations` array.

### Phase 2: Embedded Static Web UI (`backend/app/static/index.html`)
- [ ] Create directory `backend/app/static/`.
- [ ] Implement a single, clean HTML file `index.html`:
  - [ ] Structure a simple chat log interface container (with scrolling support).
  - [ ] Add text entry box and "Send" button.
  - [ ] Add "End Session" button to close the session and trigger summarization.
  - [ ] Implement vanilla javascript fetch function referencing REST endpoint POST `/chat`:
    - [ ] Append user message to log.
    - [ ] Send payload: `{"prompt": text, "thread_id": currentSessionId}`.
    - [ ] Append returned LLM `generation` text and list of formatted citations.
- [ ] Update `backend/app/main.py` to serve this static assets interface:
  - [ ] Add imports: `from fastapi.responses import HTMLResponse`.
  - [ ] Mount route `@app.get("/", response_class=HTMLResponse)` reading the local `index.html` file stream and returning it directly.
