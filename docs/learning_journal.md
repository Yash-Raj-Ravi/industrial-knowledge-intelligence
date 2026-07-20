# Day 1

## Completed
- Repository setup
- GitHub configuration
- PyCharm Pro setup
- Virtual environment
- FastAPI installation
- First API endpoint
- Swagger documentation
- First Git commit

## Concepts Learned
- FastAPI application
- Decorators
- GET endpoints
- JSON responses
- HTTP methods (GET vs POST)
- Route mapping
- Uvicorn
- API metadata (title, description, version)

## Biggest Learning
FastAPI does not execute functions automatically. Decorators register route-function mappings internally, and FastAPI calls the appropriate function when a matching HTTP request arrives.

## Next Goal
Implement PDF upload API.

# Day 2

## Completed
- Implemented generic file upload API
- Created POST `/upload` endpoint
- Supported multiple document formats (PDF, DOCX, PPTX, XLSX, CSV, TXT, PNG, JPEG)
- Added MIME type validation
- Implemented file saving to local `uploads/` directory
- Added HTTP error handling for unsupported file types
- Installed and configured `python-multipart`
- Moved application configuration to `config.py`
- Tested file uploads successfully using Swagger UI

## Concepts Learned
- UploadFile
- File(...)
- multipart/form-data
- python-multipart
- HTTPException
- File streaming
- MIME type validation
- Binary file handling (`wb`)
- shutil.copyfileobj()
- os.makedirs()
- os.path.join()
- Configuration management using `config.py`
- Multi-format document upload design

## Biggest Learning
Uploading and processing documents are two separate responsibilities. The upload API should only validate, store, and acknowledge uploaded files, while document parsing and text extraction should be handled by dedicated processing modules later in the pipeline.

## Next Goal
Implement a document parsing service starting with PDF text extraction and design the parser architecture so additional document formats can be integrated easily.

# Day 3

## Completed
- Implemented PDF document parsing using PyMuPDF
- Created `pdf_parser.py` for PDF text extraction
- Implemented page-by-page text extraction
- Ignored blank pages during parsing
- Created `parser_factory.py` for selecting parsers based on file extension
- Implemented dictionary-based parser registration
- Created `document_service.py` to coordinate document parsing
- Added POST `/parse` endpoint
- Added request validation using a Pydantic model (`ParseRequest`)
- Added file extension normalization for case-insensitive parser selection
- Implemented HTTP error handling for unsupported file types, missing files, and unexpected parsing errors
- Added character count to the parsing response
- Successfully tested PDF parsing using Swagger UI

## Concepts Learned
- PyMuPDF (`fitz`)
- PDF document object
- Page-by-page text extraction
- `page.get_text("text")`
- Context managers (`with`)
- `str.strip()`
- `"\n".join()`
- Factory Pattern
- Service Layer architecture
- Separation of concerns
- Function references in Python
- Dictionary-based dispatch
- `os.path.splitext()`
- `os.path.basename()`
- Pydantic request models (`BaseModel`)
- Exception handling (`try-except`)
- HTTP status codes (400, 404, 500)

## Biggest Learning
A clean backend architecture separates responsibilities across different layers. The API layer should handle HTTP communication, the service layer should coordinate the workflow, the factory should decide which parser to use, and each parser should focus only on extracting data from its specific document format. This modular design makes the application easier to maintain and extend with new document types.

## Next Goal
Extend the parsing pipeline by implementing parsers for additional document formats such as DOCX, PPTX, XLSX, CSV, and TXT while reusing the existing service and factory architecture.

# Day 4

## Completed
- Implemented TXT document parser (`txt_parser.py`)
- Implemented CSV document parser (`csv_parser.py`)
- Implemented DOCX document parser using `python-docx`
- Implemented PPTX document parser using `python-pptx`
- Implemented XLSX document parser using `openpyxl`
- Extracted text from Word document paragraphs
- Extracted text from PowerPoint slides and text shapes
- Extracted text from Excel worksheets row by row
- Converted CSV rows and Excel rows into plain text format
- Ignored blank paragraphs, slides, and rows during parsing
- Registered all document parsers in `parser_factory.py`
- Added type hints using `Callable` for parser functions
- Successfully tested parsing for PDF, TXT, CSV, DOCX, PPTX, and XLSX using Swagger UI

## Concepts Learned
- `python-docx`
- `python-pptx`
- `openpyxl`
- `Document()`
- `Presentation()`
- `load_workbook()`
- `document.paragraphs`
- `presentation.slides`
- `slide.shapes`
- `shape.has_text_frame`
- `sheet.iter_rows(values_only=True)`
- Generator expressions
- `",".join()`
- `Callable`
- Multi-format document parsing
- Open/Closed Principle (SOLID)
- Extensible parser architecture

## Biggest Learning
A well-designed parser architecture allows new document formats to be added with minimal changes to the existing codebase. By following the Factory Pattern and keeping every parser responsible for only one document type, the same API endpoint and service layer can support multiple file formats without modification. This demonstrates how modular software design improves scalability, maintainability, and code reuse.

## Next Goal
Implement the text chunking pipeline to split extracted document text into manageable chunks, generate metadata, and prepare the parsed content for embeddings and Retrieval-Augmented Generation (RAG).

# Day 5

## Completed

* Implemented `Chunk` data model using Pydantic to represent document chunks with metadata.
* Implemented `TextChunker` class using a character-based sliding window algorithm.
* Added configurable chunk size and chunk overlap through `config.py`.
* Implemented chunk metadata generation including `chunk_id`, `start_char`, `end_char`, `char_count`, and `word_count`.
* Added constructor validation for invalid chunk size and overlap configurations.
* Refactored `DocumentService` from a standalone function into a service class.
* Implemented `ChunkService` to coordinate document parsing and text chunking.
* Added `POST /chunk` API endpoint for generating document chunks.
* Successfully tested chunk generation for PDF, TXT, CSV, DOCX, PPTX, and XLSX documents using Swagger UI.

## Concepts Learned

* Text Chunking
* Character-based Chunking
* Sliding Window Algorithm
* Chunk Overlap
* Pydantic Models
* Object-Oriented Programming (OOP)
* Constructors (`__init__`)
* Instance Attributes (`self`)
* Service Layer Architecture
* Separation of Concerns (SoC)
* Single Responsibility Principle (SRP)
* Dependency Injection
* Metadata Generation
* Defensive Programming
* Pipeline Architecture

## Biggest Learning

A well-designed processing pipeline separates responsibilities into independent, reusable components. By isolating document parsing, text chunking, and service orchestration into dedicated classes, the system becomes easier to maintain, extend, and test. Using configurable chunk sizes and overlap through a sliding window algorithm ensures that document context is preserved while preparing high-quality chunks for embeddings and Retrieval-Augmented Generation (RAG).

## Next Goal

Implement the embedding generation pipeline by converting document chunks into vector embeddings, preparing them for storage in a vector database, and enabling semantic retrieval as the foundation of the RAG system.


# Day 6

## Completed

* Implemented `EmbeddingModel` wrapper using LangChain's `OllamaEmbeddings` for local embedding generation.
* Added configurable `EMBEDDING_MODEL` and `OLLAMA_BASE_URL` through `config.py`.
* Implemented `embed_text()` and `embed_texts()` methods for single-query and batch embedding generation.
* Implemented `ChunkEmbedding` Pydantic model to represent embedding vectors along with chunk metadata.
* Implemented `EmbeddingResponse` Pydantic model to represent the embedding generation response.
* Implemented `EmbeddingService` to coordinate document chunk embedding generation.
* Added validation for empty chunk collections before generating embeddings.
* Integrated LangChain with the locally hosted Ollama embedding model (`mxbai-embed-large`).
* Added `POST /embed` API endpoint for generating embeddings from supported document types.
* Successfully tested embedding generation for PDF, TXT, CSV, DOCX, PPTX, and XLSX documents using Swagger UI.
* Successfully verified end-to-end communication between FastAPI, LangChain, and the local Ollama server.

## Concepts Learned

* Vector Embeddings
* Semantic Embeddings
* LangChain Embeddings
* Ollama Local LLM Integration
* Batch Embedding Generation
* Embedding Dimensions
* Pydantic Response Models
* Service Layer Architecture
* Separation of Concerns (SoC)
* Single Responsibility Principle (SRP)
* Dependency Injection
* Batch Processing
* List Comprehensions
* `zip()` Function
* Type Hinting (`list[str]`, `list[list[float]]`)
* Defensive Programming
* Clean API Design
* Local AI Model Inference
* End-to-End AI Processing Pipeline

## Biggest Learning

Generating embeddings is only a small part of building an AI application. The majority of the work lies in designing a clean, modular processing pipeline that separates responsibilities between services, models, and API endpoints. By isolating embedding generation into dedicated `EmbeddingModel` and `EmbeddingService` classes and integrating them with LangChain and Ollama, the application becomes easier to maintain, test, and extend. Batch embedding generation also improves efficiency by processing multiple document chunks in a single request while preserving a clean and scalable architecture for the future RAG pipeline.

## Next Goal

Implement vector database integration using ChromaDB by storing generated embeddings along with their chunk metadata, building a document indexing pipeline, and enabling semantic similarity search as the retrieval component of the Retrieval-Augmented Generation (RAG) system.

# Day 7

## Completed

* Installed and configured ChromaDB for persistent vector storage.
* Added configurable `CHROMA_PATH` and `COLLECTION_NAME` through `config.py`.
* Implemented `ChromaStore` to manage vector database operations.
* Implemented `add_embeddings()` to store document chunks, embedding vectors, metadata, and unique UUID-based IDs in ChromaDB.
* Implemented `similarity_search()` to retrieve semantically similar document chunks using query embeddings.
* Implemented `reset_database()` utility for clearing and recreating the ChromaDB collection during development.
* Refactored `ChunkEmbedding` to contain the complete `Chunk` model instead of duplicating chunk information.
* Refactored `EmbeddingService` by renaming `generate_embeddings()` to `generate_chunk_embeddings()` for improved clarity.
* Added `generate_query_embedding()` to `EmbeddingService` for generating embeddings from user queries.
* Implemented `SearchRequest`, `ChunkMetadata`, `SearchResult`, and `SearchResponse` Pydantic models.
* Implemented `SearchService` to coordinate query embedding generation, semantic retrieval, and API response construction.
* Added `POST /search` API endpoint for semantic document retrieval.
* Successfully indexed document embeddings into ChromaDB through FastAPI.
* Successfully performed end-to-end semantic search using locally generated query embeddings.

## Concepts Learned

* ChromaDB
* Persistent Vector Databases
* Vector Indexing
* Semantic Similarity Search
* Query Embeddings
* Document Indexing Pipeline
* UUID Generation
* ChromaDB Collections
* Search Request & Response Design
* API Response Transformation
* Composition over Duplication
* Dictionary Unpacking (`**kwargs`)
* Data Transformation Layer
* Law of Demeter (Least Knowledge Principle)
* Service Layer Architecture
* Separation of Concerns (SoC)
* Single Responsibility Principle (SRP)
* Clean API Design
* Retrieval-Augmented Generation (RAG) Retrieval Pipeline
* End-to-End Semantic Retrieval Pipeline

## Biggest Learning

Building a vector database is far more than simply storing embeddings. A clean retrieval pipeline requires separating indexing, embedding generation, vector storage, and semantic search into dedicated layers with clearly defined responsibilities. By introducing `ChromaStore` and `SearchService`, the backend now hides ChromaDB's internal implementation behind clean API models, making the system easier to maintain, extend, and replace in the future. Understanding how query embeddings, vector similarity search, and response transformation work together provided a much deeper understanding of how the retrieval component of a RAG system is built.

## Next Goal

Integrate a local LLM with the semantic retrieval pipeline by constructing prompts from the retrieved document chunks, generating context-aware responses using Ollama, and completing the Retrieval-Augmented Generation (RAG) workflow.

# Day 8

## Completed

* Integrated a local LLM using Ollama with configurable `LLM_MODEL` and `OLLAMA_BASE_URL`.
* Implemented `LLMModel` to abstract communication with the local language model.
* Implemented `LLMService` to generate responses while isolating model-specific inference logic.
* Implemented `build_prompt()` utility to construct context-aware prompts from retrieved document chunks and user queries.
* Implemented `RAGRequest` and `RAGResponse` Pydantic models.
* Implemented `RAGService` to orchestrate semantic retrieval, prompt construction, LLM inference, and response generation.
* Added `POST /ask` API endpoint for Retrieval-Augmented Generation (RAG).
* Added lightweight `EmbedResponse` model to expose indexing summaries instead of returning embedding vectors.
* Added development-only `POST /reset` API endpoint for clearing and recreating the ChromaDB collection.
* Successfully completed end-to-end Retrieval-Augmented Generation using locally hosted Ollama models.
* Successfully generated grounded responses using only retrieved document context.
* Successfully validated optional source citation support with both `include_sources=true` and `include_sources=false`.
* Successfully verified graceful handling of out-of-context questions without hallucinating unsupported information.

## Concepts Learned

* Local Large Language Models (LLMs)
* Ollama
* ChatOllama
* Prompt Engineering
* Prompt Construction
* Retrieval-Augmented Generation (RAG)
* Context Injection
* LLM Inference Pipeline
* Service Orchestration
* Composition of Services
* Response Grounding
* Hallucination Prevention
* Separation of Internal and Public API Models
* API Response Design
* Early Return Pattern
* List Comprehensions
* Development Utilities for Backend Systems

## Biggest Learning

A Retrieval-Augmented Generation system is much more than simply connecting a language model to a vector database. The retrieval, prompt construction, and language generation stages should remain independent, with each component having a single well-defined responsibility. By introducing `LLMService`, `RAGService`, and a dedicated prompt builder, the backend now coordinates semantic retrieval and language generation through clean service abstractions rather than tightly coupling individual components. This made it clear that building a maintainable RAG system depends as much on software architecture and separation of concerns as it does on machine learning models.

## Next Goal

Refactor the backend using dependency injection to eliminate duplicated service instances, improve object ownership, fix vector database reset behavior, and further strengthen the overall backend architecture while preparing the project for production-oriented enhancements.

# Day 9

## Completed

* Created a dedicated `core/dependencies.py` module to centralize application dependency management.
* Implemented dependency provider functions (`get_*`) for all major services and infrastructure components.
* Integrated FastAPI's `Depends()` across backend endpoints for dependency injection.
* Refactored `EmbeddingService` to receive `EmbeddingModel` through constructor injection.
* Refactored `SearchService` to receive `EmbeddingService` and `ChromaStore` through constructor injection.
* Refactored `LLMService` to receive `LLMModel` through constructor injection.
* Refactored `RAGService` to receive `SearchService` and `LLMService` through constructor injection.
* Removed direct service instantiation from `main.py` by centralizing object creation in a dedicated composition root.
* Successfully unified all services around a shared `ChromaStore` instance.
* Successfully resolved vector database reset behavior by eliminating duplicate `ChromaStore` instances across the application.
* Successfully verified application startup after introducing constructor-based dependency injection.
* Successfully validated complete upload → embed → search → ask workflow after architectural refactoring.
* Successfully verified repeated reset → embed → search → ask cycles without requiring backend restart.

## Concepts Learned

* Dependency Injection (DI)
* Constructor Injection
* FastAPI `Depends()`
* Dependency Providers
* Composition Root
* Inversion of Control (IoC)
* Object Lifetime Management
* Shared Service Instances
* Service Composition
* Loose Coupling
* Separation of Concerns
* Single Responsibility Principle (SRP)
* Dependency Graph
* Backend Architecture
* State Management
* Production-Oriented Backend Design

## Biggest Learning

Dependency Injection is much more than replacing object creation with `Depends()`. The real benefit comes from separating object construction from business logic so that every service receives its dependencies instead of creating them itself. By introducing a centralized composition root and constructor injection, the backend now has a single source of truth for shared services and infrastructure. This not only simplified object ownership and eliminated duplicated service instances, but also resolved the ChromaDB reset issue by ensuring every component operates on the same shared vector store. The refactor demonstrated that good software architecture can solve system-level problems just as effectively as changes to application logic.

## Next Goal

Extend the document ingestion pipeline with OCR support for scanned PDFs and image-based documents, allowing the system to extract text from non-selectable documents while keeping the existing parser architecture extensible and maintainable.

# Day 10

## Completed

* Added OCR support for scanned PDF documents using Tesseract OCR.
* Created a dedicated `OCRService` (`core/ocr.py`) to encapsulate OCR functionality.
* Installed and configured Tesseract OCR Engine for text extraction from images.
* Installed and configured Poppler for converting PDF pages into images.
* Integrated `pdf2image` to convert scanned PDF pages into `PIL.Image` objects.
* Added centralized `TESSERACT_PATH` configuration within `config.py`.
* Added `OCRService` to the centralized dependency container (`core/dependencies.py`).
* Refactored `DocumentService` to receive `OCRService` through constructor injection.
* Refactored `ChunkService` to receive `DocumentService` through constructor injection, maintaining a fully dependency-injected service layer.
* Modified the PDF parser to receive `OCRService` as a dependency instead of creating it internally.
* Implemented a hybrid PDF parsing strategy that first attempts native text extraction using PyMuPDF and automatically falls back to OCR for pages without extractable text.
* Optimized OCR execution by converting only the required PDF page into an image instead of rendering the entire document.
* Successfully verified standalone OCR extraction from image files.
* Successfully validated searchable PDFs using native text extraction without invoking OCR.
* Successfully validated fully scanned PDFs using automatic OCR fallback.
* Successfully verified hybrid PDFs containing both searchable and scanned pages.
* Successfully confirmed complete upload → parse → chunk → embed → search → ask workflow after OCR integration.

## Concepts Learned

* Optical Character Recognition (OCR)
* Tesseract OCR Engine
* Poppler
* pdf2image
* PIL (Pillow)
* Hybrid Document Parsing
* Fallback Processing
* Native Text Extraction vs OCR
* Searchable PDF vs Scanned PDF
* Per-Page Processing
* Lazy Resource Processing
* Dependency Injection in Parser Architecture
* Configuration Management
* Extensible Backend Design

## Biggest Learning

OCR integration is much more than simply extracting text from images. A robust document ingestion pipeline should first use the fastest and most accurate extraction method available before falling back to OCR only when necessary. By combining native text extraction with page-level OCR fallback, the backend now supports searchable, scanned, and hybrid PDF documents while avoiding unnecessary image conversion and OCR processing. This implementation demonstrated how clean architecture and dependency injection allow significant new functionality to be added without affecting downstream components such as chunking, embeddings, semantic search, or RAG generation.

## Next Goal

Develop a user-friendly frontend for the Industrial Knowledge Intelligence platform using Streamlit, enabling users to upload heterogeneous industrial documents, interact with the RAG-powered knowledge base through a conversational interface, visualize retrieved source citations, and manage the document repository through an intuitive workflow. This will transform the backend into a complete working prototype while significantly improving usability, demonstration quality, and overall project readiness for the hackathon evaluation.

# Day 11

## Completed

* Developed the initial Streamlit frontend for the Industrial Knowledge Intelligence platform.
* Created a dedicated frontend `config.py` to centralize application settings, backend URL, API endpoints, and request timeout configuration.
* Created a reusable frontend API layer (`api.py`) for communicating with the FastAPI backend.
* Implemented backend health check functionality to verify API availability from the frontend.
* Developed the main Streamlit application (`app.py`) with application branding, welcome page, and backend status indicator.
* Developed the **Upload Documents** page for document ingestion.
* Added document selection using `st.file_uploader()` with support for PDF, TXT, CSV, PPTX, DOCX, and XLSX documents.
* Added document information cards displaying filename, file size, and document type before upload.
* Integrated the complete upload → embed workflow through the frontend using FastAPI endpoints.
* Added upload progress indication using `st.spinner()`.
* Implemented success and error handling for document upload and indexing operations.
* Developed the **Chat with Knowledge Base** page using Streamlit's native chat components.
* Implemented persistent conversation history using `st.session_state`.
* Added a reusable `ask_question()` API wrapper for communicating with the backend RAG endpoint.
* Integrated the conversational interface with the backend to support document-grounded question answering.
* Successfully verified complete end-to-end workflow from document upload to conversational retrieval through the frontend.

## Concepts Learned

* Streamlit Application Architecture
* Streamlit Multi-Page Applications
* Streamlit Session State
* `st.file_uploader()`
* `st.chat_input()`
* `st.chat_message()`
* `st.spinner()`
* Frontend API Abstraction Layer
* REST API Integration using Requests
* Separation of Presentation and Business Logic
* Frontend Configuration Management
* State Persistence in Streamlit
* Conversational UI Design
* End-to-End Frontend–Backend Integration

## Biggest Learning

Building the frontend involved much more than creating user interfaces. A well-designed frontend should remain independent of backend implementation details by communicating through a dedicated API abstraction layer while maintaining application state separately from presentation logic. Using Streamlit's session state and modular page architecture demonstrated how an interactive conversational interface can be built with minimal complexity while preserving clean separation between the frontend, backend services, vector database, and language model. This resulted in a complete end-to-end RAG application capable of document ingestion and conversational knowledge retrieval through a user-friendly interface.

## Next Goal

Enhance the frontend by implementing document source citation visualization, improving metadata returned from semantic search, developing repository management features, integrating `streamlit-option-menu` for a more professional navigation experience, and refining the overall user interface to create a polished, hackathon-ready demonstration of the Industrial Knowledge Intelligence platform.

# Day 12

## Completed

* Extended the document upload workflow to support uploading multiple documents simultaneously using Streamlit's `accept_multiple_files` feature.
* Added batch document indexing with upload progress visualization.
* Enhanced the chat interface by grouping retrieved source citations according to their originating documents.
* Added relevance score calculation and display for retrieved document chunks.
* Implemented document-level citation grouping with highest relevance score for each retrieved document.
* Refactored prompt construction to include document names and balanced retrieved context by limiting the number of chunks contributed by each document.
* Developed a reusable **Sidebar** component displaying backend status and repository statistics across all frontend pages.
* Implemented dynamic suggested questions generated from indexed repository documents.
* Added adaptive suggested questions that automatically change based on the number of indexed documents.
* Added clickable suggested question buttons for initiating conversations directly from the chat interface.
* Added contextual empty-state handling for the chat page when no documents are indexed.
* Added simulated streaming responses to improve conversational user experience.
* Developed the **Repository** page for viewing indexed documents.
* Added repository statistics showing total indexed documents and total stored chunks.
* Displayed indexed documents as information cards with file-type icons, document type, and chunk count.
* Implemented backend repository management using a dedicated `RepositoryService`.
* Added repository endpoint for retrieving indexed document metadata from ChromaDB.
* Implemented **Reset Knowledge Base** functionality through the frontend.
* Added confirmation checkbox to prevent accidental repository reset operations.
* Successfully validated complete multi-document Retrieval-Augmented Generation (RAG) workflow through the frontend.

## Concepts Learned

* Multi-file Upload using `st.file_uploader()`
* Streamlit Progress Components
* Source Citation Visualization
* Metadata Aggregation from Vector Databases
* Repository Management
* Reusable Streamlit Components
* Dynamic UI Generation
* Conditional Rendering in Streamlit
* Streamlit Sidebar Components
* Semantic Search Result Presentation
* Retrieval Context Balancing
* ChromaDB Metadata Processing
* Simulated Response Streaming
* Multi-Document Retrieval-Augmented Generation (RAG)

## Biggest Learning

A production-ready Retrieval-Augmented Generation system requires much more than retrieving relevant chunks from a vector database. Presenting grouped citations, balancing retrieved context across multiple documents, exposing repository management features, and providing contextual user guidance significantly improve usability without modifying the underlying retrieval pipeline. Building reusable frontend components and dynamically adapting the interface based on repository state demonstrated how thoughtful UI design can greatly enhance the overall user experience while preserving a modular backend architecture.

## Next Goal

Extend the Industrial Knowledge Intelligence platform to support OCR directly from image files by implementing dedicated image parsers for PNG, JPG, and JPEG formats, integrate camera capture through Streamlit, and route both uploaded images and captured photos through the existing OCR → Chunking → Embedding → ChromaDB → RAG pipeline, enabling conversational querying over image-based industrial documents.

# Day 13

## Completed

* Implemented on-demand entity extraction for indexed documents through the Repository page.
* Added dedicated backend endpoint for extracting entities from individual documents using document identifiers.
* Refactored entity extraction workflow to retrieve document file paths dynamically from ChromaDB metadata.
* Extended document embedding metadata to include original file paths for repository operations.
* Implemented individual document deletion functionality using document identifiers.
* Added backend support for deleting individual documents from ChromaDB without resetting the entire knowledge base.
* Integrated document deletion into the Repository page with a confirmation dialog to prevent accidental removal.
* Added document search functionality for filtering indexed documents by filename.
* Enhanced repository statistics to dynamically update based on filtered search results.
* Improved repository interface by hiding empty entity categories during entity visualization.
* Added Markdown chat history export functionality.
* Implemented reusable chat export utility for generating downloadable conversation transcripts.
* Added timestamped chat export filenames for improved history management.
* Refactored retrieved source citation rendering into a reusable helper function.
* Improved chat interface by displaying retrieved source citations immediately after streamed responses.
* Performed UI refinements across the Repository and Chat pages to improve overall usability and maintainability.

## Concepts Learned

* Document-level Repository Management
* ChromaDB Metadata-Based Operations
* Entity Extraction Workflows
* Document Deletion in Vector Databases
* Streamlit Dialog Components (`@st.dialog`)
* Search and Filtering in Streamlit
* Dynamic Repository Statistics
* Markdown File Generation
* Chat History Export
* Reusable UI Helper Functions
* Code Refactoring for Maintainability
* Streamlit Download Components (`st.download_button`)

## Biggest Learning

Managing a Retrieval-Augmented Generation system extends beyond document retrieval and question answering. Features such as document lifecycle management, on-demand entity extraction, repository search, conversation export, and reusable UI components significantly improve the usability and maintainability of the application. Separating repository operations into dedicated services while reusing frontend components demonstrated how modular design enables new functionality to be added with minimal impact on the existing RAG pipeline.

## Next Goal

Polish the Industrial Knowledge Intelligence platform by improving the overall user interface, enhancing documentation, refining error handling, performing end-to-end testing, and preparing the application for deployment and demonstration as Version 1.0.