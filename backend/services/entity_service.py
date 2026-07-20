import json

from backend.llm.llm_model import LLMModel


class EntityService:
    def __init__(self, llm_model: LLMModel):
        self.llm_model = llm_model

    def extract_entities(self, text: str) -> dict:

        prompt = f"""
You are an industrial document analysis assistant.

Extract important entities from the document.

Return ONLY valid JSON in exactly this format:

{{
    "equipment": [],
    "personnel": [],
    "locations": [],
    "procedures": [],
    "standards": [],
    "dates": []
}}

Rules:
- Do not invent information.
- Remove duplicates.
- Return only JSON.
- Do not use markdown.
- If a category is absent, return an empty list.

Document:

{text}
"""

        try:
            response = self.llm_model.generate(prompt)

            # Remove markdown fences if present
            response = response.replace("```json", "").replace("```", "").strip()

            entities = json.loads(response)

            for key in [
                "equipment",
                "personnel",
                "locations",
                "procedures",
                "standards",
                "dates",
            ]:
                entities.setdefault(key, [])

            return entities

        except Exception:
            return {
                "equipment": [],
                "personnel": [],
                "locations": [],
                "procedures": [],
                "standards": [],
                "dates": [],
            }