from ..services.document_service import DocumentService
from ..services.chunk_service import ChunkService
from ..services.embedding_service import EmbeddingService
from ..services.search_service import SearchService
from ..services.rag_service import RAGService
from ..services.repository_service import RepositoryService
from ..vectorstore.chroma_store import ChromaStore
from ..embedding.embedding_model import EmbeddingModel
from ..services.llm_service import LLMService
from ..llm.llm_model import LLMModel
from ..core.ocr import OCRService
from fastapi import Depends

# leading underscore is used to indicate these are private module-level instances:

_store = ChromaStore()
_embedding_model = EmbeddingModel()
_embedding_service = EmbeddingService(_embedding_model)
_search_service = SearchService(
    _embedding_service,
    _store,
)
_llm_model = LLMModel()
_llm_service = LLMService(_llm_model)

_ocr_service = OCRService()
_document_service = DocumentService(_ocr_service)
_chunk_service = ChunkService(_document_service)
_rag_service = RAGService(
    _search_service,
    _llm_service,
)

def get_document_service():
    return _document_service

def get_chunk_service():
    return _chunk_service

def get_embedding_service():
    return _embedding_service

def get_rag_service():
    return _rag_service

def get_search_service():
    return _search_service

def get_chroma_store():
    return _store

def get_ocr_service():
    return _ocr_service

def get_repository_service(
    store: ChromaStore = Depends(get_chroma_store)
):
    return RepositoryService(store)