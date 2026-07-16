from pydantic import BaseModel
from backend.models.chunk import Chunk

class ChunkEmbedding(BaseModel):
    chunk : Chunk
    embedding: list[float]
    dimension: int
    file_name: str
    document_type: str
    document_id : str

class EmbeddingResponse(BaseModel):
    total_chunks: int
    embeddings: list[ChunkEmbedding]
    embedding_dimension: int

class EmbedResponse(BaseModel):
    message: str
    total_chunks: int
    embedding_dimension: int

class ResetResponse(BaseModel):
    message: str