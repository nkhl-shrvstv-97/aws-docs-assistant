# RAG Pipeline Architecture

This document details the design and implementation of both the **Ingestion Pipeline** (document preprocessing and indexing) and the **Retrieval Pipeline** (fetching context during query execution).

---

## 1. Ingestion Pipeline (Logical & Technical Flow)

The ingestion pipeline is designed to transform raw, unstructured HTML pages downloaded from the live AWS Documentation into high-density Markdown text with metadata, chunked and embedded in PostgreSQL.

```text
  [Live HTML URLs] ──► [Local download_docs.py] ──► [Markdown Files with YAML Frontmatter]
                                                                  │
                                                                  ▼ (Sync to S3 bucket)
                                                        [S3 Document Landing Zone]
                                                                  │
                                                                  ▼ (Upload event trigger)
                                                         [Amazon SQS Queue]
                                                                  │
                                                                  ▼ (Throttled Concurrency)
                                                        [AWS Lambda Ingestion Worker]
                                                                  │
                                            ┌─────────────────────┴─────────────────────┐
                                            ▼ (Parse Frontmatter Metadata)              ▼ (Split & Embed Body)
                                     URL, Title, Service                        MarkdownTextSplitter 
                                            │                                           │
                                            └─────────────────────┬─────────────────────┘
                                                                  ▼
                                                      [RDS PostgreSQL pgvector]
```

### A. Document Source & Preprocessing (Local Phase)
1. **Source Generation:** A local utility Python script fetches live HTML pages from target AWS Documentation URLs using `requests` and parses content inside the `<div id="main-content">` node.
2. **Markdown Conversion:** The HTML content is cleaned of scripts and navigation blocks, and converted into Markdown using the `markdownify` package.
3. **YAML Frontmatter Prepends:** A structured YAML metadata block is prepended to the top of each Markdown file before uploading it to S3:
   ```markdown
   ---
   title: "Creating an Amazon S3 Bucket"
   url: "https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html"
   service: "AmazonS3"
   ---
   # Creating an Amazon S3 Bucket
   ...
   ```

### B. Ingestion Scaling & Database Protection (AWS Phase)
1. **Landing Zone & Events:** Markdown files are uploaded to an Amazon S3 bucket. Each upload triggers an event mapped to an **Amazon SQS Queue**.
2. **Concurrency Throttling:** AWS Lambda processes messages from the SQS queue in small batches (e.g., concurrency capped at 15-20 parallel runs). This allows massive parallel uploads while protecting the RDS database connection pool.
3. **Lambda Worker Action:** The Lambda worker downloads the `.md` file, parses the YAML Frontmatter metadata block, and feeds the Markdown body to the chunking splitter.

### C. Chunking Strategy (Markdown Preserving)
* **Splitter:** LangChain's `MarkdownTextSplitter`.
* **Configuration:**
  * **Chunk Size:** 1000 characters.
  * **Chunk Overlap:** 200 characters.
* **Why Markdown?** Unlike recursive text splitters that cut lines arbitrarily, the `MarkdownTextSplitter` respects markdown boundaries (such as section headings `#`, `##` and table structures `| Col 1 |`). This keeps code blocks, lists, and tables intact within individual chunks, preserving context.

### D. Vector Generation & Storage
1. **Embedding Model:** `amazon.titan-embed-text-v2:0` via Bedrock.
2. **Parameters:**
   * **Dimensions:** 1536
   * **Normalize:** True
3. **Database Insertion:** Inserts the chunk content, metadata values, and embedding vectors into the `document_chunks` table in RDS PostgreSQL.

---

## 2. Retrieval Pipeline

The retrieval pipeline executes inside the LangGraph workflow to gather appropriate context.

```text
    Standalone Query
           │
           ▼
 [Titan Text Embeddings] (1536 dims)
           │
           ▼
  [pgvector Cosine Match] (HNSW Index Search)
           │
           ▼
    [Document Grader] (Relevance filtering)
           │
           ▼
   [Final Context Stack]
```

### A. Core Search Execution
* **Embedding Conversion:** Converts the `standalone_query` into a 1536-dimensional float vector using Titan Embeddings.
* **SQL Query Execution:**
  ```sql
  SELECT content, source_url, title, service_name, (embedding <=> :query_embedding) AS distance
  FROM document_chunks
  ORDER BY distance ASC
  LIMIT 5;
  ```
  * Note: `<=>` represents cosine distance in `pgvector`.

### B. Fallback Documentation Search
When local retrieval returns zero relevant documents (detected by the `grade_documents` node):
1. The agent invokes the **AWS Doc Search Tool**.
2. This tool calls an external web search API (e.g. Tavily or Google Search) restricted to `site:docs.aws.amazon.com`.
3. The scraper retrieves the content from the top 2-3 links, runs the parser, chunks the text dynamically, and appends it to the context window.

---

## 3. Database Schema

```sql
CREATE EXTENSION IF NOT EXISTS vector;

-- Document chunks vector database table
CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding VECTOR(1536), -- 1536 dimensions for Amazon Titan Multimodal/Text Embeddings V2
    source_url TEXT NOT NULL,
    title TEXT NOT NULL,
    service_name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ON document_chunks USING hnsw (embedding vector_cosine_ops);

-- Session summaries for long term agent memory
CREATE TABLE IF NOT EXISTS session_summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(100) UNIQUE NOT NULL,
    summary TEXT NOT NULL,                   -- LLM generated summary
    topics VARCHAR(255)[] NOT NULL,          -- Array of detected AWS services/topics
    embedding VECTOR(1536),                  -- Embed summary for semantic retrieval
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ON session_summaries USING hnsw (embedding vector_cosine_ops);
```

---

## 4. Future Production Scaling Enhancements

To scale this baseline pipeline into an enterprise RAG system, the following architectural upgrades would be implemented:

### A. Hierarchical / Parent-Child Chunking
* **The Concept:** Standard chunking forces a trade-off: small chunks are better for vector matching (less noise), but large chunks provide better context to the LLM (no lost details).
* **Implementation:** Store small "child" chunks (e.g. 200 tokens) with embedding vectors in the DB, linked via a foreign key relation to a larger "parent" document chunk (e.g. 1500 tokens). When a match hits the child chunk, the system retrieves and feeds the parent document context to the generator LLM.

### B. Visual Table and Layout Parsing
* **The Concept:** Complex AWS docs feature structural matrices, diagrams, and architecture flowcharts that pure text splitters lose.
* **Implementation:** Use a layout-aware parser (such as LlamaParse or unstructured.io) to compile visual components. Tables are converted into clean structured JSON tables, and architectural images are run through multimodal Vision LLMs (e.g. Claude 3.5 Sonnet Vision) to generate text captions indexed alongside the document text.

### C. Hybrid Search & Cross-Encoder Re-ranking
* **The Concept:** Dense vector search struggles with specific keyword tokens (such as error codes, parameter flags, or exact CLI commands).
* **Implementation:** 
  1. Perform dual retrieval: **Dense semantic search** (using Titan Embeddings) + **Sparse lexical search** (using BM25 search matching keywords).
  2. Combine results using Reciprocal Rank Fusion (RRF).
  3. Send the top 20 documents to a **Cross-Encoder Re-ranker** (such as Cohere Rerank) to compute a high-fidelity relevance score, bubbling the top 5 most useful blocks to the prompt.

---

## 5. How to Trigger the Ingestion Pipeline

To run the unified scraper and automatically upload the compiled documents to your AWS S3 landing bucket (which then triggers the SQS and Lambda pipeline), execute the following commands:

```bash
# 1. Export the target S3 bucket name (generated by Terraform output)
export S3_BUCKET_NAME="nikhil-aws-docs-assistant-landing-[your-unique-suffix]"

# 2. Execute the runner script using the uv environment
PYTHONPATH=. .venv/bin/python backend/ingestion/run_ingest_pipeline.py
```

