from backend.models.repository import RepositoryResponse
from backend.vectorstore.chroma_store import ChromaStore


class RepositoryService:
    def __init__(self,store: ChromaStore) :
        self.store = store

    def get_repository(self) -> RepositoryResponse:
        data = self.store.list_documents()

        return RepositoryResponse(**data)