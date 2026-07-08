from backend.models.search import SearchRequest, SearchResponse , SearchResult , ChunkMetadata
from backend.services.embedding_service import EmbeddingService
from backend.vectorstore.chroma_store import ChromaStore

class SearchService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.store = ChromaStore()

    def search(self, request:SearchRequest) -> SearchResponse:
        if self.store.collection.count() == 0:
            raise ValueError("No documents have been indexed yet.")
        
        query_embedding = self.embedding_service.generate_query_embedding(request.query)
        chroma_results = self.store.similarity_search(query_embedding,request.top_k)

        documents = chroma_results["documents"][0]
        metadatas = chroma_results["metadatas"][0]
        distances = chroma_results["distances"][0]

        results = []

        for doc,meta,dist in zip(documents,metadatas,distances):
            results.append(
                SearchResult(
                    text = doc,
                    distance = dist,
                    metadata = meta
                )
            )
        return SearchResponse(
            total_results = len(results),
            results = results
        )





