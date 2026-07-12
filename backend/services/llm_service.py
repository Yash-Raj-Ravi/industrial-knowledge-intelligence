# LLMService should do only one thing:
# Given a prompt, ask Ollama to generate a response and return it.

from backend.llm.llm_model import LLMModel

class LLMService:
    def __init__(self, llm_model: LLMModel):
        self.llm_model = llm_model

    def generate_response(self,prompt:str) -> str:
        return self.llm_model.generate(prompt)