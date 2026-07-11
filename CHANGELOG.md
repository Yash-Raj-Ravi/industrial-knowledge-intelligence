# Changelog

All notable changes to this project will be documented in this file.

---

## [0.1.0] - Day 1 (30 June 2026)

### Added
- Initialized the GitHub repository.
- Created the project folder structure.
- Set up the Python virtual environment.
- Initialized the FastAPI backend.
- Added the first API endpoint (`GET /`).
- Added project documentation (`README.md`).
- Added dependency management with `requirements.txt`.

### Project Status
- Backend foundation completed.
- Ready to implement document ingestion and PDF upload pipeline.

---

## [0.2.0] - Day 2 (1 July 2026)

### Added
- Implemented generic document upload API (`POST /upload`).
- Added support for multiple document formats (PDF, DOCX, PPTX, XLSX, CSV, TXT, PNG, JPEG).
- Added MIME type validation for uploaded files.
- Implemented local file storage in the `uploads/` directory.
- Added automatic upload directory creation.
- Added HTTP error handling for unsupported file types.
- Added `python-multipart` dependency for handling file uploads.
- Created `config.py` to centralize application configuration.

### Changed
- Refactored configuration values (upload directory and allowed file types) into `config.py`.
- Improved project structure by separating configuration from application logic.

### Project Status
- Multi-format document ingestion service completed.
- Ready to implement document parsing and text extraction pipeline.

---

## [0.3.0] - Day 3 (3 July 2026)

### Added
- Implemented PDF document parser using PyMuPDF.
- Created a dedicated PDF parsing module (`pdf_parser.py`).
- Implemented a parser factory (`parser_factory.py`) for selecting parsers based on file extension.
- Created a document service layer (`document_service.py`) to orchestrate document parsing.
- Added the `POST /parse` API endpoint for extracting text from uploaded documents.
- Added request validation using a Pydantic model (`ParseRequest`).
- Added exception handling for unsupported file types, missing files, and unexpected parsing errors.
- Added case-insensitive file extension handling for parser selection.
- Added character count to the parsing API response.

### Changed
- Adopted a layered architecture by separating API, service, factory, and parser responsibilities.
- Improved project modularity to simplify future support for additional document formats.

### Project Status
- PDF text extraction pipeline completed.
- Clean and extensible document parsing architecture established.
- Ready to implement parsers for DOCX, PPTX, XLSX, CSV, TXT, and OCR support.


---

## [0.4.0] - Day 4 (4 July 2026)

### Added
- Implemented TXT document parser (`txt_parser.py`).
- Implemented CSV document parser (`csv_parser.py`).
- Implemented DOCX document parser using `python-docx` (`docx_parser.py`).
- Implemented PPTX document parser using `python-pptx` (`pptx_parser.py`).
- Implemented XLSX document parser using `openpyxl` (`xlsx_parser.py`).
- Registered all document parsers in the parser factory for automatic parser selection.
- Added parser type hints using `Callable` for improved code readability and IDE support.

### Changed
- Extended the document parsing pipeline to support multiple document formats through the existing service and factory architecture.
- Improved the parser factory to provide a single, extensible entry point for all supported document types without modifying the API or service layer.
- Reused the existing `POST /parse` endpoint to process all supported document formats.

### Tested
- Successfully verified text extraction for PDF, TXT, CSV, DOCX, PPTX, and XLSX documents through Swagger UI.

### Project Status
- Multi-format document parsing pipeline completed.
- Extensible parser architecture established for adding future document types with minimal code changes.
- Ready to implement text chunking and document preprocessing for the RAG pipeline.

## [0.5.0] - Day 5 (5 July 2026)

### Added

* Implemented `Chunk` data model using Pydantic to represent document chunks with metadata.
* Implemented `TextChunker` class for reusable text chunking.
* Added configurable character-based chunking with chunk size and overlap.
* Added chunk metadata generation including `chunk_id`, `start_char`, `end_char`, `char_count`, and `word_count`.
* Added validation for invalid chunk size and overlap configurations.
* Implemented `ChunkService` to coordinate document parsing and text chunking.
* Added `POST /chunk` API endpoint to generate chunks from supported document types.

### Changed

* Refactored `DocumentService` from a standalone function into a service class for improved modularity and consistency with the project architecture.
* Separated document parsing and text chunking responsibilities into dedicated service and processing layers.
* Configured the chunking pipeline to use centralized `CHUNK_SIZE` and `CHUNK_OVERLAP` values from the application configuration.
* Improved code readability with stronger type hints and object-oriented design.

### Tested

* Successfully verified the chunking pipeline for PDF, TXT, CSV, DOCX, PPTX, and XLSX documents through Swagger UI.
* Verified correct chunk metadata generation, configurable chunk size, overlap behavior, and total chunk count across supported document formats.

### Project Status

* Document ingestion pipeline completed through text chunking.
* Modular service architecture established with `DocumentService`, `TextChunker`, and `ChunkService`.
* Documents can now be uploaded, parsed, and converted into structured chunks ready for embedding generation.
* Ready to implement embeddings, vector storage, and semantic retrieval for the RAG pipeline.


## [0.6.0] - Day 6 (6 July 2026)

### Added

* Implemented `EmbeddingModel` wrapper using LangChain's `OllamaEmbeddings` for local embedding generation.
* Added configurable `EMBEDDING_MODEL` and `OLLAMA_BASE_URL` through `config.py`.
* Implemented `embed_text()` and `embed_texts()` methods for single-query and batch embedding generation.
* Implemented `ChunkEmbedding` Pydantic model to represent chunk embeddings with associated metadata.
* Implemented `EmbeddingResponse` Pydantic model to represent embedding generation results.
* Implemented `EmbeddingService` to coordinate batch embedding generation from document chunks.
* Added validation for empty chunk collections before embedding generation.
* Added `POST /embed` API endpoint to generate embeddings for supported document types using the local Ollama embedding model.

### Changed

* Refactored the project structure by moving the `Chunk` Pydantic model into the centralized `backend/models` package.
* Extended the document processing pipeline from parsing and chunking to semantic embedding generation.
* Improved code readability through clearer variable naming and stronger separation between embedding vectors and response models.
* Optimized embedding dimension calculation by computing it once per embedding batch and reusing the value throughout the response.

### Tested

* Successfully verified local Ollama integration using the `mxbai-embed-large` embedding model.
* Successfully generated embeddings for PDF, TXT, CSV, DOCX, PPTX, and XLSX documents through Swagger UI.
* Verified correct embedding generation for every document chunk.
* Verified embedding dimensions, chunk metadata preservation, and batch embedding generation.
* Confirmed successful communication between FastAPI, LangChain, and the local Ollama server.

### Project Status

* Semantic embedding generation pipeline completed.
* Modular AI backend architecture established with `DocumentService`, `ChunkService`, `EmbeddingService`, and `EmbeddingModel`.
* Documents can now be uploaded, parsed, chunked, and converted into vector embeddings using a locally hosted embedding model.
* Ready to integrate ChromaDB for vector storage, document indexing, semantic retrieval, and the complete Retrieval-Augmented Generation (RAG) pipeline.

# Day 7

## Added

* Installed and configured **ChromaDB** for persistent vector storage.
* Added configurable `CHROMA_PATH` and `COLLECTION_NAME` through `config.py`.
* Implemented `ChromaStore` to manage vector database operations.
* Implemented `add_embeddings()` to persist document embeddings, metadata, and documents into ChromaDB.
* Implemented `similarity_search()` to perform semantic retrieval using query embeddings.
* Implemented `reset_database()` utility for clearing and recreating the ChromaDB collection during development.
* Implemented `SearchRequest`, `ChunkMetadata`, `SearchResult`, and `SearchResponse` Pydantic models.
* Implemented `SearchService` to coordinate semantic search by generating query embeddings, retrieving relevant chunks, and formatting the response.
* Added `POST /search` API endpoint for semantic document retrieval.

## Changed

* Refactored `EmbeddingService` by renaming `generate_embeddings()` to `generate_chunk_embeddings()` for clearer intent.
* Added `generate_query_embedding()` to `EmbeddingService` for generating embeddings from user queries while preserving service-layer abstraction.
* Refactored `ChunkEmbedding` to use composition by embedding the complete `Chunk` model instead of duplicating chunk fields.
* Improved service-layer separation by ensuring `SearchService` communicates with `EmbeddingService` instead of directly accessing `EmbeddingModel`.
* Decoupled the public API from ChromaDB's internal response format by transforming raw search results into strongly typed response models.

## Tested

* Successfully verified persistent storage of document embeddings in ChromaDB.
* Verified automatic creation of the persistent `chroma_db` database.
* Confirmed successful indexing of document chunks with unique UUID-based identifiers.
* Successfully tested database reset functionality and collection recreation.
* Verified semantic similarity search using query embeddings generated by the local Ollama embedding model.
* Successfully validated end-to-end indexing and retrieval through FastAPI Swagger UI.
* Confirmed retrieval of the most semantically relevant document chunks with associated metadata and similarity distances.

## Project Status

* Persistent vector database integration completed.
* Semantic document indexing pipeline completed.
* End-to-end semantic retrieval pipeline completed.
* Backend now supports uploading, parsing, chunking, embedding, indexing, and semantic search over multiple document formats.
* Clean service-oriented architecture established with `DocumentService`, `ChunkService`, `EmbeddingService`, `SearchService`, `EmbeddingModel`, and `ChromaStore`.
* Ready to integrate a local LLM for Retrieval-Augmented Generation (RAG), prompt construction, and context-aware answer generation.

# Day 8

## Added

* Integrated a local LLM using **Ollama** with configurable `LLM_MODEL` and `OLLAMA_BASE_URL`.
* Implemented `LLMModel` to abstract interactions with the local language model.
* Implemented `LLMService` to generate responses from prompts while isolating model-specific inference logic.
* Implemented `build_prompt()` utility for constructing context-aware prompts using retrieved document chunks and user queries.
* Implemented `RAGRequest` and `RAGResponse` Pydantic models.
* Implemented `RAGService` to orchestrate semantic retrieval, prompt construction, LLM inference, and response generation.
* Added `POST /ask` API endpoint for Retrieval-Augmented Generation (RAG).
* Added lightweight `EmbedResponse` model to expose indexing summaries instead of embedding vectors.
* Added development-only `POST /reset` API endpoint for clearing and recreating the ChromaDB collection.

## Changed

* Refactored the embedding endpoint to return concise indexing metadata instead of exposing internal embedding vectors.
* Improved API design by separating internal embedding models from public response models.
* Refactored the RAG pipeline into dedicated retrieval, prompt construction, and language model layers.
* Implemented optional source citation support through the `include_sources` request parameter.
* Improved service-layer orchestration by ensuring `RAGService` coordinates existing services instead of directly implementing retrieval or inference logic.

## Tested

* Successfully verified end-to-end Retrieval-Augmented Generation using locally hosted Ollama models.
* Confirmed semantic retrieval of the most relevant document chunks before answer generation.
* Verified prompt construction using retrieved context and user queries.
* Successfully validated grounded answer generation using only information from indexed documents.
* Confirmed correct handling of out-of-context questions without hallucinating unsupported information.
* Verified optional source citation support with both `include_sources=true` and `include_sources=false`.
* Successfully validated the complete upload → embed → ask workflow through FastAPI Swagger UI.
* Confirmed ChromaDB persistence across application restarts.
* Identified duplicate retrieval behaviour caused by repeated indexing of identical documents during development.

## Project Status

* End-to-end Retrieval-Augmented Generation (RAG) pipeline completed.
* Backend now supports document upload, parsing, chunking, embedding generation, vector indexing, semantic retrieval, prompt construction, and grounded answer generation using a local LLM.
* Service-oriented architecture expanded with `LLMModel`, `LLMService`, and `RAGService` while maintaining clear separation of concerns.
* Public API now exposes complete semantic question-answering functionality through the `POST /ask` endpoint.
* Development utilities added for vector database management and simplified iterative testing.
* Ready for architectural refinements including dependency injection, retrieval filtering, and production-oriented backend improvements.