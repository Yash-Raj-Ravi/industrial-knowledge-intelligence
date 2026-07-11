def build_prompt(chunks:list[str],query:str) -> str:
    context = "\n\n".join(chunks)

    prompt = f"""You are an AI assistant. Answer the user's question using ONLY the information provided in the context below.
    If the answer cannot be found in the context, say: "I don't have enough information in the provided documents."
    
    Context: 
    {context}
    Question: 
    {query}
    Answer: 
    """
    return prompt