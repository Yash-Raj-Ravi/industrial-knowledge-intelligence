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