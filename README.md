# AWS Docs Assistant: Production-Grade Agentic Chatbot & RAG Pipeline

An enterprise-ready Agentic Chatbot designed to interact with official AWS Documentation using advanced Retrieval-Augmented Generation (RAG) and LLM agentic orchestration. 

This repository demonstrates production-quality software engineering, clean architecture, and modern agentic AI practices for a technical assessment. It is fully deployable to AWS via Terraform Infrastructure as Code (IaC).

Live Deployed UI URL: [INSERT_DEPLOYED_UI_URL_HERE](INSERT_DEPLOYED_UI_URL_HERE)

---

## Architecture Overview & Documentation Index

Detailed implementation details are separated into modular documentation guides:

1. **[LangGraph Agent Architecture](docs/agent-architecture.md)**
   * Outlines the multi-step state graph: Domain classification, query rewriting, local database retrieval, relevance grading, fallback live search, grounding verification, and retry loops.
2. **[RAG Pipeline Architecture](docs/rag-architecture.md)**
   * Details HTML cleaning, MarkdownTextSplitter semantic chunking, dynamic pgvector HNSW cosine matching, and the S3-SQS-Lambda document ingestion flow.
3. **[Terraform & Cloud Infrastructure](docs/terraform-architecture.md)**
   * Describes the secure AWS networking layout (VPC public/private isolation), RDS PostgreSQL configuration, Secrets Manager auto-credential mapping, and serverless hosting via App Runner.
4. **[Directory Structure & Application Layout](docs/directory-structure.md)**
   * Map of modules, schemas, endpoints, and deployment roles in the codebase.

---

## Key Features and Capabilities

* **Long-Term Semantic Memory (Session Summarization):** When a user ends a session (via the UI "End Session" button or CLI exit), the agent automatically compiles a structured session summary, embeds it, and stores it in RDS. In subsequent sessions, if the user asks contextual questions (e.g., "What did we talk about last time?"), the agent dynamically pulls these vector summaries into the prompt context to maintain continuity.
* **LangGraph Orchestration & Corrective RAG:** The decision loop runs on a LangGraph workflow. It includes a classification node to filter out-of-scope prompts, a document grader to evaluate retrieved content, and an anti-hallucination grounding grader that loops back to refine generation or execute fallback searches if response claims are unsupported by retrieved documentation chunks.
* **Hybrid Context Retrieval:**
  * **Local Vector Store:** High-performance semantic queries over local documentation using PostgreSQL pgvector HNSW cosine similarity matching and amazon.titan-embed-text-v2:0.
  * **Live Search Fallback:** Live web-scraping fallback tool restricted to site:docs.aws.amazon.com for queries not answered by the local database.
* **SlowAPI Rate Limiting:** public API endpoints are protected using SlowAPI rate-limiting filters to control usage, defend against burst-traffic attacks, and prevent runaway Bedrock consumption costs.
* **LangSmith Observability Integration:** Full out-of-the-box integration with LangSmith tracing. Simply configure standard LangChain environment variables to capture detailed trace visualizations of state transitions, node latency, and model input/output pairs.
* **S3/SQS/Lambda Ingestion Queueing:** An event-driven ingestion pipeline where document uploads to Amazon S3 publish event notifications to an SQS Queue. A throttled Lambda function (max concurrency cap of 2, batch size of 5) pulls from the queue to run chunking and database insertions, shielding the RDS PostgreSQL connection pool.
* **VPC Network Isolation:** Secure networking layout containing public and private subnets. The RDS instances have no public IPs and strictly allow TCP port 5432 ingress only from App Runner and Lambda security groups.
* **Automatic Database Schema Initialization:** The FastAPI application utilizes SQLAlchemy models to automatically run migrations and initialize required database tables on startup.
* **Interactive UI & CLI Interfaces:** Includes an embedded, lightweight single-page HTML/JS interface served natively by FastAPI, alongside a CLI terminal application (cli.py) with session management hooks.
* **Comprehensive Test Suite:** Includes unit and integration tests (test_agent.py, test_rag_pipeline.py) utilizing pytest to validate agent state transitions, prompt formatting, document chunking, and mock Bedrock API calls.

---

## Tech Stack

* **Backend & API:** Python 3.11+, FastAPI, Uvicorn, SlowAPI, SQLAlchemy (ORM)
* **Agent Framework:** LangGraph, LangChain AWS (Bedrock Integration)
* **LLM & Embeddings:** Amazon Bedrock (anthropic.claude-3-5-sonnet-v2, anthropic.claude-3-haiku, amazon.titan-embed-text-v2:0)
* **Database:** Amazon RDS PostgreSQL + pgvector extension
* **Infrastructure:** Terraform, AWS App Runner, AWS Lambda, Amazon S3, Amazon SQS, AWS Secrets Manager, VPC Security Groups

---

## Local Development Quickstart

For full configuration and seeding details, please refer to the architecture guides. Below is the minimal startup sequence:

```bash
# Clone the repository and setup venv
git clone <your-repo-url>
cd aws-docs-assistant
python3 -m venv .venv && source .venv/bin/activate && pip install -r backend/requirements.txt

# Run crawler & ingestion (requires local PostgreSQL with pgvector)
PYTHONPATH=. python backend/ingestion/download_docs.py
PYTHONPATH=. python backend/ingestion/ingest.py

# Start FastAPI API server
PYTHONPATH=. uvicorn backend.app.main:app --reload
```

---

## AWS Production Deployment & Cleanup

The entire environment is configured to deploy with zero manual setup in AWS Console using Terraform.

### 1. Provision Infrastructure
Ensure your terminal is authenticated with your target AWS account credentials, then execute:
```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
```

Upon successful deployment, Terraform will export:
* `app_runner_url`: The public endpoint of the hosted FastAPI chatbot.
* `s3_bucket_name`: The landing S3 bucket for uploading document files.
* `rds_endpoint`: The private RDS PostgreSQL instance endpoint.

### 2. Trigger Ingest Pipeline
To sync crawled AWS documentation to S3 and trigger the automatic Lambda ingestion worker:
```bash
export S3_BUCKET_NAME="your-terraform-s3-bucket-name"
PYTHONPATH=. python backend/ingestion/run_ingest_pipeline.py
```

### 3. Cleanup / Destroy Infrastructure
Once the solution has been reviewed and tested, execute the following command to completely destroy all provisioned AWS resources and avoid incurring any further costs:
```bash
cd terraform
terraform destroy -auto-approve
```

---

## Production Gaps & Future Roadmap

The following enterprise features were omitted due to the assignment time constraints:
* **User Authentication & Multi-Tenancy:** Integration of OAuth2/OIDC (e.g., AWS Cognito) with row-level security (RLS) in PostgreSQL to partition thread histories by user.
* **Distributed Caching (Redis):** Caching semantic search matches and common LLM query responses to reduce system latency and Bedrock processing costs.
* **Resilience Patterns (Circuit Breakers):** Implementing fallback paths (e.g., using `tenacity` or `resilience4j` structures) to gracefully handle Bedrock throttle exceptions or search engine downtime.
* **Production-Grade Rate Limiting:** Migrating SlowAPI from in-memory storage to a shared Redis backend to manage rates across scaled App Runner compute containers.
* **Hybrid Search & Re-ranking:** Combining standard vector search with keyword-based lexical search (BM25) and feeding the results into a Cross-Encoder Re-ranker (e.g., Cohere/BGE) to optimize context relevance.
* **CI/CD Pipelines:** Automated pipelines (e.g., GitHub Actions) to run the pytest suite, compile Docker containers, push to AWS ECR, and execute Terraform plans.

---

## Testing

To run unit and integration tests (validating query translation, chunk relevance grading, and agent schema routing):
```bash
pytest backend/tests/
```
