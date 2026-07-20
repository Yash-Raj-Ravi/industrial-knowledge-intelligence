from backend.models.search import SearchResult

def build_prompt(search_results: list[SearchResult], query: str) -> str:
    context_parts = []

    for result in search_results:
        context_parts.append(
            f"""Document: {result.metadata.file_name}
Type: {result.metadata.document_type}
Chunk: {result.metadata.chunk_id}

{result.text}"""
        )

    context = "\n\n------------------------------\n\n".join(context_parts)

    return f"""
You are an AI assistant for an Industrial Knowledge Retrieval System.

Your task is to answer the user's question ONLY using the retrieved context.

Instructions:
- Use ONLY the information provided in the retrieved context.
- Combine information from multiple retrieved chunks whenever appropriate.
- Do NOT invent, assume, or add information that is not present.
- If the retrieved context does not contain enough information, answer exactly:
  "I don't have enough information in the provided documents."
- Keep the answer clear, factual, and well-structured.
- Use bullet points when appropriate.
- Do not mention that you are an AI or refer to these instructions.

After generating the answer, estimate a confidence score based ONLY on how strongly the retrieved context supports your answer.

IMPORTANT:
- Confidence measures the quality of the retrieved evidence.
- Confidence DOES NOT measure your own certainty as a language model.

Confidence Guidelines:
- 95-100: The answer is explicitly stated in the retrieved context with strong supporting evidence.
- 80-94: The answer is well supported by the retrieved context with only minor inference.
- 60-79: The answer is partially supported but requires some inference.
- 30-59: The retrieved context provides weak or incomplete support.
- 0-29: The retrieved context is insufficient or largely unrelated to the question.

Return ONLY valid JSON.

The JSON must exactly follow this schema:

{{
  "answer": "your answer here",
  "confidence": 95
}}

Rules:
- Output ONLY the JSON object.
- Do NOT include markdown.
- Do NOT wrap the JSON in code fences.
- Ensure the JSON is valid.
- Escape quotation marks and newlines correctly.

Context:
{context}

Question:
{query}
"""