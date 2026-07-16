import streamlit as st
from config import APP_TITLE
from api import check_backend
from components.sidebar import render_sidebar

render_sidebar()

def main():
    st.title(f"🏭 {APP_TITLE}")

    st.caption("AI-powered industrial knowledge retrieval using Retrieval-Augmented Generation (RAG).")

    with st.container():
        st.subheader("Welcome")

        st.write(
            """
            This platform enables you to:
    
            - 📄 Upload heterogeneous industrial documents
            - 🔍 Perform semantic search across the knowledge base
            - 🤖 Interact using an AI-powered chat interface
            - 📚 View retrieved source citations
            - 🧠 Utilize a local RAG pipeline powered by Ollama and ChromaDB
            """
        )

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏭",
    layout="wide"
)

if __name__ == "__main__":
    main()
