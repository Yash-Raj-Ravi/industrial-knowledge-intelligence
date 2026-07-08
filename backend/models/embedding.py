from pydantic import BaseModel
from backend.models.chunk import Chunk

class ChunkEmbedding(BaseModel):
    chunk : Chunk
    embedding: list[float]
    dimension: int

class EmbeddingResponse(BaseModel):
    total_chunks: int
    embeddings: list[ChunkEmbedding]
    embedding_dimension: int
