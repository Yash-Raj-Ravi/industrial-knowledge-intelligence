from langchain_ollama import OllamaEmbeddings
from backend.config import EMBEDDING_MODEL,OLLAMA_BASE_URL

class EmbeddingModel:
    def __init__(self):
        self.model = OllamaEmbeddings(
            model = EMBEDDING_MODEL,
            base_url = OLLAMA_BASE_URL
        )

    def embed_text(self,text: str) -> list[float]:  # Query embedding
        return self.model.embed_query(text)

    def embed_texts(self,texts: list[str]) -> list[list[float]]: # Document Chunks embedding
        return self.model.embed_documents(texts)





