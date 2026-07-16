from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"

ALLOWED_TYPES = {"application/pdf",

                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # DOCX

                 "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # PPTX

                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # XLSX

                 "text/plain",

                 "text/csv",

                 "image/png",

                 "image/jpeg"
                 }
# Chunking 
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# Embedding Configuration
EMBEDDING_MODEL = "mxbai-embed-large:latest"
OLLAMA_BASE_URL = "http://localhost:11434"

# Vector database
CHROMA_PATH = BASE_DIR / "chroma_db"
COLLECTION_NAME = "industrial_documents"

# LLM
LLM_MODEL = "llama3.1:8b"

# OCR
TESSERACT_PATH = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")

MAX_CHUNKS_PER_DOCUMENT = 3