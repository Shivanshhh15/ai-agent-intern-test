# Aster & Row — Reliable RAG Support Agent

A lightweight Retrieval-Augmented Generation (RAG) support agent built for the Aster & Row ecommerce support use case.

The system retrieves relevant information from a curated knowledge base and produces grounded support answers with source attribution. It is designed to avoid hallucinating information when the knowledge base does not contain an answer.

---

## Features

- Markdown knowledge-base ingestion
- YAML front-matter metadata support
- Heading-aware document chunking
- Local semantic embeddings using Sentence Transformers
- Persistent ChromaDB vector database
- Semantic similarity search
- Policy-aware retrieval for returns, shipping and warranty questions
- Source attribution
- Unknown-question / hallucination protection
- No paid API dependency for the RAG pipeline
- Command-line evaluation scripts
- Pytest-based automated tests

---

## Architecture

```text
                    Knowledge Base
                         |
                         v
                  Markdown Loader
                         |
                         v
                    Chunker
                         |
                         v
              Sentence Transformers
                  Local Embeddings
                         |
                         v
                     ChromaDB
                         |
                         v
                    Retriever
                         |
                         v
                  Support Agent
                         |
              +----------+----------+
              |          |          |
           Returns    Shipping   Warranty
              |          |          |
              +----------+----------+
                         |
                         v
                  Grounded Answer
                         |
                         v
                  Source Attribution


---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Shivanshhh15/ai-agent-intern-test.git
cd ai-agent-intern-test