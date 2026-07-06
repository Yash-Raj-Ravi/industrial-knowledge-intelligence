from pydantic import BaseModel

class ChunkEmbedding(BaseModel):
    chunk_id: int
    embedding: list[float]
    dimension: int
    char_count: int
    word_count: int

class EmbeddingResponse(BaseModel):
    total_chunks: int
    embeddings: list[ChunkEmbedding]
    embedding_dimension: int
