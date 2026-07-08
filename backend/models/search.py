from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str
    top_k: int = 4

class ChunkMetadata(BaseModel):
    chunk_id: int
    start_char: int
    end_char: int
    char_count: int
    word_count: int

class SearchResult(BaseModel):
    text: str
    distance: float
    metadata: ChunkMetadata

class SearchResponse(BaseModel):
    total_results : int
    results: list[SearchResult]
