from langchain_ollama import ChatOllama
from backend.config import LLM_MODEL,OLLAMA_BASE_URL

class LLMModel:
    def __init__(self):
        self.model = ChatOllama(
            model = LLM_MODEL,
            base_url = OLLAMA_BASE_URL,
            temperature=0
        )

    def generate(self,prompt:str) -> str:
        response = self.model.invoke(prompt)
        return response.content.strip()