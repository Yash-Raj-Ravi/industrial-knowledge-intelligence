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

Answer the user's question using ONLY the information provided in the context.

Instructions:
- Use information from ALL relevant context snippets whenever applicable.
- If multiple documents discuss different aspects of the question, combine the information into a single coherent answer.
- Do not make up information that is not present in the context.
- If the question asks to compare concepts, summarize information from all relevant retrieved documents before drawing conclusions.
- Answer clearly and concisely.
- Use bullet points or short paragraphs when appropriate.
- If the question contains multiple parts, answer each part separately whenever the context contains sufficient information.
- Avoid repeating the same information if it appears in multiple context snippets.
- If the context does not contain enough information, reply:
  "I don't have enough information in the provided documents."

Context:
{context}

Question:
{query}

Answer:
"""