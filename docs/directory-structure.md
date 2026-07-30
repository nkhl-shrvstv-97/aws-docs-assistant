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
