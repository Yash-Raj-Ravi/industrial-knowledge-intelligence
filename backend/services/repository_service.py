from backend.models.repository import RepositoryResponse
from backend.vectorstore.chroma_store import ChromaStore


class RepositoryService:
    def __init__(self,store: ChromaStore) :
        self.store = store

    def get_repository(self) -> RepositoryResponse:
        data = self.store.list_documents()

        return RepositoryResponse(**data)

    def get_file_path(self, document_id: str) -> str:
        return self.store.get_file_path(document_id)

    def delete_document(self, document_id: str):
        self.store.delete_document(document_id)