# Take-Home Assignment

## Overview

This repository contains the implementation of a take-home assignment for an AI/LLM Engineering role.

The objective is to build a production-quality **Agentic Chatbot** that enables users to interact with AWS Documentation using modern LLM techniques. The solution should demonstrate expertise in Agentic AI, Retrieval-Augmented Generation (RAG), cloud-native development, Infrastructure as Code (IaC), and scalable software engineering.

The implementation should prioritize clean architecture, extensibility, maintainability, and production-readiness over simply delivering a working prototype.

---

# Original Assignment

## Objective

Build an **Agentic Chatbot** that allows users to interact with **AWS Documentation** through a sophisticated natural language interface.

## Expectations

The solution should demonstrate:

- Strong understanding of LLM-based applications
- Agentic workflow implementation
- Retrieval-Augmented Generation (RAG) concepts
- Natural language query handling
- Integration and interaction with AWS documentation
- Clean architecture and scalable design practices

---

# Deliverables

The final submission should include:

- Complete source code
- Infrastructure as Code (Terraform)
- GitHub repository
- Documentation
- Deployment instructions
- Architecture documentation
- Setup instructions

---

# Assignment Context

The company has provided:

- A dedicated AWS test account
- Amazon Bedrock access
- Access to foundation models through Bedrock
- A clean AWS environment for deployment
- A requirement to provision infrastructure using Terraform

The following observations have already been made:

## Available

- Amazon Bedrock
- Foundation models (confirmed via Bedrock Playground)
- Terraform deployment

## Not Available

- No AWS documentation dataset
- No S3 bucket containing documentation
- No Bedrock Knowledge Base
- No OpenSearch domain
- No EC2 instances
- No ECR repositories

The AWS account should therefore be treated as a clean environment where all application infrastructure is provisioned by this project.

---

# Clarification Received

A clarification was requested regarding the expected scope of the AWS documentation corpus for the RAG pipeline.

The response from the interviewer was:

> You can make your own assumptions.

Therefore, the architecture should be driven by engineering judgment rather than attempting to satisfy an explicitly prescribed implementation.

---

# Design Assumptions

Based on the clarification received, the following assumptions will guide the implementation.

## Knowledge Base

The chatbot will **not** attempt to ingest the entirety of AWS documentation.

Instead, it will:

- Build a complete RAG pipeline over a representative subset of AWS documentation.
- Keep the ingestion pipeline generic and extensible so additional documentation can be indexed without architectural changes.

## Agentic Retrieval Strategy

The system should demonstrate both:

- Retrieval-Augmented Generation (RAG)
- Agentic tool selection

The agent will have access to multiple retrieval mechanisms.

### Tool 1 — Local Knowledge Base (Primary)

A locally indexed vector database containing a representative subset of AWS documentation.

Responsibilities:

- Semantic retrieval
- Context retrieval
- Citation generation
- Low-latency responses

### Tool 2 — Live AWS Documentation Search (Fallback)

When the planner determines that the required information is not available in the indexed knowledge base, it may invoke a documentation search tool to retrieve relevant AWS documentation before generating the final answer.

This allows the chatbot to answer questions beyond the locally indexed corpus while still demonstrating a complete RAG implementation.

The local RAG pipeline remains the primary retrieval mechanism.

---

# Primary Objectives

The implementation should demonstrate proficiency in:

- Agentic AI
- Retrieval-Augmented Generation (RAG)
- LLM orchestration
- Tool calling
- AWS cloud services
- Infrastructure as Code
- Production software engineering
- Scalable system architecture

---

# Functional Requirements

The chatbot should support:

- Natural language conversations
- Multi-turn chat
- Conversation history
- Semantic retrieval
- Source citations
- Context-aware answers
- Hallucination mitigation
- Follow-up questions
- Dynamic tool selection by the planner

---

# Non-Functional Requirements

The solution should prioritize:

- Modular architecture
- Scalability
- Extensibility
- Maintainability
- Testability
- Observability
- Configuration management
- Security best practices

---

# Planned Technology Stack

## Backend

- Python
- FastAPI

## Agent Framework

- LangGraph
- LangChain (only where appropriate)

## LLM

- Amazon Bedrock
- Foundation model available through Bedrock

## Retrieval

- Document ingestion pipeline
- Chunking
- Embedding generation
- Vector database
- Semantic retrieval
- Metadata filtering
- Citation support

## Agent Tools

- Local RAG Retriever
- AWS Documentation Search Tool

## Infrastructure

- Terraform
- AWS
- Docker

## Development

- Git
- Pytest
- Structured logging
- Environment-based configuration

---

# Engineering Principles

The implementation should follow:

- SOLID principles
- Clean Architecture
- Separation of concerns
- Dependency injection where appropriate
- Infrastructure as Code
- Configuration over hardcoded values
- Production-oriented design
- Extensible agent architecture

---

# Out of Scope

Unless additional requirements emerge, the following are intentionally out of scope:

- Fine-tuning foundation models
- Multi-region deployment
- High availability
- Multi-tenancy
- CI/CD pipelines
- Horizontal auto-scaling

These may be documented as future improvements.

---

# Success Criteria

A successful implementation should clearly demonstrate:

1. A production-quality agentic chatbot.
2. A complete Retrieval-Augmented Generation pipeline.
3. Intelligent tool selection by the planner.
4. Effective interaction with AWS documentation.
5. Integration with Amazon Bedrock.
6. Infrastructure provisioned using Terraform.
7. Clean, modular, and extensible architecture.
8. Comprehensive documentation explaining all major architectural and implementation decisions.