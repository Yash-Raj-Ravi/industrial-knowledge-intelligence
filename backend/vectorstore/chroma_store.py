import chromadb
from backend.config import CHROMA_PATH, COLLECTION_NAME
from backend.models.embedding import ChunkEmbedding
import uuid
#from pprint import pprint

class ChromaStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = self.client.get_or_create_collection(COLLECTION_NAME)

    def add_embeddings(self, chunk_embeddings : list[ChunkEmbedding]) -> list[str]:
        documents = [
            ce.chunk.text for ce in chunk_embeddings # ce -> ChunkEmbedding
        ]

        embedding_vectors = [
            ce.embedding for ce in chunk_embeddings
        ]

        metadatas = [
            {
                "chunk_id": ce.chunk.chunk_id,
                "start_char": ce.chunk.start_char,
                "end_char": ce.chunk.end_char,
                "char_count": ce.chunk.char_count,
                "word_count": ce.chunk.word_count
            }
            for ce in chunk_embeddings
        ]

        ids = [
                str(uuid.uuid4())+ '_' + str(ce.chunk.chunk_id)
                for ce in chunk_embeddings
              ]

        self.collection.add(
            ids = ids,
            documents = documents,
            embeddings = embedding_vectors,
            metadatas = metadatas
        )

        return ids

    def reset_database(self):
        try:
           self.client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(COLLECTION_NAME)

    def similarity_search(self,query_embedding : list[float], top_k: int = 4):

        results = self.collection.query(query_embeddings = [query_embedding],
                                        n_results = top_k,
                                        include = ["documents",
                                                 "metadatas",
                                                 "distances"])
        #pprint(results)
        return results
