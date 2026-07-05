from fastapi import FastAPI,UploadFile,File,HTTPException
import os
import shutil
from .config import ALLOWED_TYPES, UPLOAD_DIR
from pydantic import BaseModel
from .services.document_service import DocumentService
from .services.chunk_service import ChunkService

app = FastAPI(title="Industrial Knowledge Intelligence API",
description="Backend API for Industrial Knowledge Intelligence Platform",
version="0.5.0")

document_service = DocumentService()
chunk_service = ChunkService()
os.makedirs(UPLOAD_DIR,exist_ok=True)

class FilePathRequest(BaseModel):
    file_path: str
@app.get("/")
def home():
    return {"message":"Industrial-knowledge-intelligence API is running",
             "status":"success"}

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    file_path = os.path.join(UPLOAD_DIR,file.filename)
    with open(file_path,"wb") as destination:
     shutil.copyfileobj(file.file,destination)
    return {"message":"File is uploaded successfully",
             "file_name":file.filename,
             "content_type":file.content_type,
             "path":file_path}

@app.post("/parse")
def parse_document_endpoint(request: FilePathRequest):
    try:
        text = document_service.parse_document(request.file_path)

        return {"message": "Document Parsed Successfully",
                "file_path":request.file_path,
                "character_count":len(text),
                "text":text}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chunk")
def chunk_doc_endpoint(request: FilePathRequest):
    try:
        chunks = chunk_service.chunk_document(request.file_path)
        return {"message": "Document Chunked Successfully",
                "file_path":request.file_path,
                "chunks":chunks,
                "total_chunks":len(chunks)
                }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



