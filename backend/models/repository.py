from pydantic import BaseModel

class DocumentInfo(BaseModel):
    document_id: str
    file_name: str
    document_type: str
    total_chunks: int

class RepositoryResponse(BaseModel):
    total_documents: int
    total_chunks: int
    documents: list[DocumentInfo]

class DeleteDocumentResponse(BaseModel):
    message: str