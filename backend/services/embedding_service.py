from backend.embedding.embedding_model import EmbeddingModel
from backend.models.chunk import Chunk
from backend.models.embedding import ChunkEmbedding,EmbeddingResponse

class EmbeddingService:

     def __init__(self):
         self.embedding_model = EmbeddingModel()

     def generate_embeddings(self,chunks:list[Chunk]) -> EmbeddingResponse:
         if not chunks:
             raise ValueError("cannot generate embeddings for empty list of chunks")
         texts = [chunk.text for chunk in chunks]

         embedding_vectors = self.embedding_model.embed_texts(texts)

         chunk_embeddings = []
         embedding_dimension = len(embedding_vectors[0])
         for chunk,embedding in zip(chunks,embedding_vectors):
             chunk_embeddings.append(ChunkEmbedding
                                     (
                 chunk_id = chunk.chunk_id,
                 embedding = embedding,
                 dimension = embedding_dimension,
                 char_count = chunk.char_count,
                 word_count = chunk.word_count
             ))
         return EmbeddingResponse(
             total_chunks = len(chunks),
             embeddings = chunk_embeddings,
             embedding_dimension = embedding_dimension
         )



