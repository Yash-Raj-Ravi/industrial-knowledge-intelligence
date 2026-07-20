from pydantic import BaseModel
from backend.models.search import SearchResult

class RAGRequest(BaseModel):
    query: str
    top_k:int = 10
    include_sources:bool = True

class RAGResponse(BaseModel):
    answer:str
    confidence: float | None = None
    sources:list[SearchResult] | None = None

