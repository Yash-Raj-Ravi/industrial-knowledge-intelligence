from pydantic import BaseModel

class DocumentInfo(BaseModel):
    file_name: str
    document_type: str
    total_chunks: int

class RepositoryResponse(BaseModel):
    total_documents: int
    total_chunks: int
    documents: list[DocumentInfo]