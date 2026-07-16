from fastapi import FastAPI,UploadFile,File,HTTPException
import shutil
import os,uuid
from .services.chunk_service import ChunkService
from .services.document_service import DocumentService
from .services.embedding_service import EmbeddingService
from .services.search_service import SearchService
from .vectorstore.chroma_store import ChromaStore
from .models.rag import RAGResponse, RAGRequest
from .models.search import SearchResponse, SearchRequest
from .config import ALLOWED_TYPES, UPLOAD_DIR
from pydantic import BaseModel
from .models.embedding import EmbedResponse, ResetResponse
from .services.rag_service import RAGService
from fastapi import Depends
# Services
from .core.dependencies import (
    get_document_service,
    get_chunk_service,
    get_embedding_service,
    get_chroma_store,
    get_search_service,
    get_rag_service,
    get_repository_service
)

from .models.repository import RepositoryResponse
from .services.repository_service import RepositoryService

app = FastAPI(
    title="Industrial Knowledge Intelligence API",
    description="Backend API for Industrial Knowledge Intelligence Platform",
    version="0.8.0"
    )


UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

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

    file_path = UPLOAD_DIR / file.filename
    with open(file_path,"wb") as destination:
     shutil.copyfileobj(file.file,destination)
    return {"message":"File is uploaded successfully",
             "file_name":file.filename,
             "content_type":file.content_type,
             "path": str(file_path)}

@app.post("/parse")
def parse_document_endpoint(request: FilePathRequest,
                            document_service: DocumentService = Depends(get_document_service)):
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
def chunk_doc_endpoint(request: FilePathRequest,
                       chunk_service: ChunkService = Depends(get_chunk_service)):
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


@app.post("/embed",
          response_model = EmbedResponse)
def embed_endpoint(request: FilePathRequest,
                   embedding_service: EmbeddingService = Depends(get_embedding_service),
                   chunk_service: ChunkService = Depends(get_chunk_service),
                   store: ChromaStore = Depends(get_chroma_store)
                   ):
    try:
        document_id = str(uuid.uuid4())
        file_name = os.path.basename(request.file_path)
        chunks = chunk_service.chunk_document(request.file_path)
        embeddings = embedding_service.generate_chunk_embeddings(chunks,file_name=file_name,document_id = document_id)


        store.add_embeddings(embeddings.embeddings)

        return EmbedResponse(
        message="Successfully indexed document.",
        total_chunks=embeddings.total_chunks,
        embedding_dimension=embeddings.embedding_dimension
    )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", response_model = SearchResponse)
def search_endpoint(request: SearchRequest,
                    search_service: SearchService = Depends(get_search_service)):
    try:
        return search_service.search(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask",response_model = RAGResponse)
def ask_endpoint(request: RAGRequest,
                 rag_service: RAGService = Depends(get_rag_service)):
    try:
        return rag_service.answer_query(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/documents",
    response_model=RepositoryResponse
)
def documents_endpoint(
    repository_service: RepositoryService = Depends(get_repository_service)
):
    try:
        return repository_service.get_repository()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Development utility endpoint.
# Clears the entire ChromaDB collection.
@app.post("/reset", response_model=ResetResponse)
def reset_database_endpoint(store: ChromaStore = Depends(get_chroma_store)):
    try:
        store.reset_database()

        return ResetResponse(
            message="Vector database reset successfully."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


