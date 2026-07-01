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

