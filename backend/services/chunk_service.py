from backend.services.document_service import DocumentService
from backend.chunking.text_chunker import TextChunker
from backend.config import CHUNK_SIZE,CHUNK_OVERLAP
from backend.chunking.models import Chunk

class ChunkService:

    def __init__(self):
        self.document_service = DocumentService()
        self.chunker = TextChunker(
            CHUNK_SIZE,
            CHUNK_OVERLAP
        )

    def chunk_document(self, file_path: str) -> list[Chunk]:
        text = self.document_service.parse_document(file_path)
        chunks = self.chunker.chunk_text(text)
        return chunks






