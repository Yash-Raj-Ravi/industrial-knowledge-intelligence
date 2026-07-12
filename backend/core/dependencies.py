from ..services.document_service import DocumentService
from ..services.chunk_service import ChunkService
from ..services.embedding_service import EmbeddingService
from ..services.search_service import SearchService
from ..services.rag_service import RAGService
from ..vectorstore.chroma_store import ChromaStore
from ..embedding.embedding_model import EmbeddingModel
from ..services.llm_service import LLMService
from ..llm.llm_model import LLMModel

# leading underscore is used to indicate these are private module-level instances:
_document_service = DocumentService()
_chunk_service = ChunkService()
_store = ChromaStore()
_embedding_model = EmbeddingModel()
_embedding_service = EmbeddingService(_embedding_model)
_search_service = SearchService(
    _embedding_service,
    _store,
)
_llm_model = LLMModel()
_llm_service = LLMService(_llm_model)

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