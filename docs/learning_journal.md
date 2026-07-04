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