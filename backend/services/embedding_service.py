from backend.embedding.embedding_model import EmbeddingModel
from backend.models.chunk import Chunk
from backend.models.embedding import ChunkEmbedding,EmbeddingResponse
import os

class EmbeddingService:
     def __init__(self, embedding_model: EmbeddingModel):
         self.embedding_model = embedding_model

     def generate_chunk_embeddings(self,chunks:list[Chunk],file_name:str,document_id:str) -> EmbeddingResponse:
         if not chunks:
             raise ValueError("cannot generate embeddings for empty list of chunks")
         texts = [chunk.text for chunk in chunks]

         embeddings = self.embedding_model.embed_texts(texts)
         document_type = os.path.splitext(file_name)[1].lower()
         chunk_embeddings = []
         embedding_dimension = len(embeddings[0])
         for chunk,embedding in zip(chunks,embeddings):
             chunk_embeddings.append(ChunkEmbedding
                                     (
                 chunk = chunk,
                 embedding = embedding,
                 dimension = embedding_dimension,
                 file_name=file_name,
                 document_type = document_type,
                 document_id = document_id

             ))
         return EmbeddingResponse(
             total_chunks = len(chunks),
             embeddings = chunk_embeddings,
             embedding_dimension = embedding_dimension
         )

     def generate_query_embedding(self,query:str) -> list[float]:
         embedding = self.embedding_model.embed_text(query)
         return embedding





