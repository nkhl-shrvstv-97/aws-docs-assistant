# AWS Docs Assistant - Implementation Documentation Index

This directory contains the detailed specifications, design assets, schemas, and configurations for implementing the production-quality Agentic Chatbot for AWS Documentation.

The documentation has been modularly separated into the following sections:

## 📂 Architecture Specifications

1. **[LangGraph Agent Architecture](file:///Users/nikhilshrivastava/Desktop/code/repos/aws-docs-assistant/agent-architecture.md)**
   * State variables schema definitions.
   * Comprehensive graph execution node logic.
   * State flow chart using Mermaid.

2. **[RAG Pipeline Architecture](file:///Users/nikhilshrivastava/Desktop/code/repos/aws-docs-assistant/rag-architecture.md)**
   * HTML/Markdown loading and cleaning strategies.
   * Chunking limits, character overlaps, and semantic headers.
   * Cosine distance query matching with PostgreSQL `pgvector`.
   * Complete database schema configurations.

3. **[Directory Structure & Application Layout](file:///Users/nikhilshrivastava/Desktop/code/repos/aws-docs-assistant/directory-structure.md)**
   * Project folder layout (FastAPI, Ingestion tools, Terraform).
   * Module component guides (routing, nodes, tools, db).

4. **[Terraform & Cloud Infrastructure Architecture](file:///Users/nikhilshrivastava/Desktop/code/repos/aws-docs-assistant/terraform-architecture.md)**
   * VPC network setups and subnet isolation.
   * Security groups, Secrets Manager credentials mapping, and IAM roles.
   * Infrastructure hosting configurations using serverless AWS App Runner and Lambda ingestion workers.
