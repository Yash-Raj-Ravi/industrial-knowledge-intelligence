# Industrial Knowledge Intelligence Platform

An AI-powered platform for industrial document intelligence, semantic knowledge retrieval, and Retrieval-Augmented Generation (RAG) using locally hosted AI models.

---

## Problem Statement

Industrial organizations manage thousands of documents such as operating procedures, maintenance manuals, inspection reports, safety guidelines, and technical documentation. Finding accurate information quickly is difficult because these documents are often distributed across multiple systems and formats.

This project aims to build an intelligent AI platform that indexes industrial documents, performs semantic search, and answers user questions using Retrieval-Augmented Generation (RAG).

---

## Current Features

### Document Processing

- Multi-format document upload
- PDF parsing using PyMuPDF
- TXT parsing
- CSV parsing
- DOCX parsing
- PPTX parsing
- XLSX parsing

### AI Processing Pipeline

- Document chunking using a sliding window approach
- Local embedding generation using Ollama (`mxbai-embed-large`)
- Batch embedding generation
- Persistent vector storage with ChromaDB
- Semantic similarity search
- Metadata-preserving document indexing

### Backend API

- File upload endpoint
- Document parsing endpoint
- Chunk generation endpoint
- Embedding generation endpoint
- Semantic search endpoint

---

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic

### AI & NLP

- LangChain
- Ollama
- ChromaDB

### Document Processing

- PyMuPDF
- python-docx
- python-pptx
- openpyxl

### Frontend (Planned)

- Streamlit

### OCR (Planned)

- Tesseract OCR

### Knowledge Graph (Planned)

- NetworkX / Neo4j

---

## Project Architecture

```text
User
 │
 ▼
Upload Document
 │
 ▼
Document Parsing
 │
 ▼
Text Chunking
 │
 ▼
Embedding Generation (Ollama)
 │
 ▼
ChromaDB Vector Store
 │
 ▼
Semantic Retrieval
 │
 ▼
RAG (Upcoming)
```

---

## Project Structure

```text
industrial-knowledge-intelligence/

├── backend/
│   ├── chunking/
│   ├── embedding/
│   ├── models/
│   ├── parsers/
│   ├── services/
│   ├── vectorstore/
│   ├── __init__.py
│   ├── config.py
│   └── main.py
│
├── data/
├── docs/
│   └── learning_journal.md
│
├── frontend/
│   └── .gitkeep
│
├── .gitignore
├── CHANGELOG.md
├── README.md
└── requirements.txt

> **Note:** The `uploads/` and `chroma_db/` directories are created automatically at runtime and are excluded from version control via `.gitignore`.
```

---

## Current Progress

### Completed

- [x] Project setup
- [x] FastAPI backend
- [x] Multi-format document upload
- [x] Multi-format document parsing
- [x] Document chunking pipeline
- [x] Local embedding generation (Ollama)
- [x] ChromaDB vector database integration
- [x] Semantic document indexing
- [x] Semantic similarity search

### In Progress

- [ ] Retrieval-Augmented Generation (RAG)
- [ ] Prompt engineering
- [ ] Local LLM integration

### Planned

- [ ] OCR support
- [ ] Camera-based document capture
- [ ] Voice input
- [ ] Drawing/P&ID upload
- [ ] Mobile-friendly interface
- [ ] Knowledge graph generation
- [ ] Deployment

---

## Roadmap

- ✅ Document ingestion
- ✅ Semantic indexing
- ✅ Vector database integration
- ✅ Semantic retrieval
- 🔄 Retrieval-Augmented Generation (RAG)
- ⏳ Industrial knowledge graph
- ⏳ Intelligent maintenance assistant
- ⏳ Production deployment

---

## Learning Objectives

This project is being built to gain practical experience with:

- FastAPI backend development
- Service-oriented architecture
- Retrieval-Augmented Generation (RAG)
- LangChain
- Ollama
- ChromaDB
- Vector databases
- Semantic search
- Local LLM deployment
- Production-ready AI system design

---

## License

This project is developed for learning, research, and hackathon purposes.
