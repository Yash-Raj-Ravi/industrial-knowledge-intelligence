from backend.embedding.embedding_model import EmbeddingModel
from backend.models.chunk import Chunk
from backend.models.embedding import ChunkEmbedding,EmbeddingResponse

class EmbeddingService:

     def __init__(self):
         self.embedding_model = EmbeddingModel()

     def generate_chunk_embeddings(self,chunks:list[Chunk]) -> EmbeddingResponse:
         if not chunks:
             raise ValueError("cannot generate embeddings for empty list of chunks")
         texts = [chunk.text for chunk in chunks]

         embeddings = self.embedding_model.embed_texts(texts)

         chunk_embeddings = []
         embedding_dimension = len(embeddings[0])
         for chunk,embedding in zip(chunks,embeddings):
             chunk_embeddings.append(ChunkEmbedding
                                     (
                 chunk = chunk,
                 embedding = embedding,
                 dimension = embedding_dimension,

             ))
         return EmbeddingResponse(
             total_chunks = len(chunks),
             embeddings = chunk_embeddings,
             embedding_dimension = embedding_dimension
         )

     def generate_query_embedding(self,query:str) -> list[float]:
         embedding = self.embedding_model.embed_text(query)
         return embedding





