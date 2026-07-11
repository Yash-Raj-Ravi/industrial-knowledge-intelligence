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