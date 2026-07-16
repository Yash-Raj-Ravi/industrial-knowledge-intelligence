import streamlit as st
from api import ask_question, get_documents
from components.sidebar import render_sidebar
from pathlib import Path
import time

render_sidebar()

st.title("💬 Chat with Knowledge Base")

st.caption(
    "Ask questions about your indexed industrial documents using Retrieval-Augmented Generation (RAG)."
)


def clean_name(file_name: str) -> str:
    """
    Removes extensions and formats file names for display.
    """

    name = Path(file_name).stem

    # Remove nested extensions like .pptx.pdf
    while "." in name:
        name = Path(name).stem

    return name.replace("_", " ")


def generate_suggestions(documents):

    if not documents:
        return []

    # Largest documents first
    documents = sorted(
        documents,
        key=lambda doc: doc["total_chunks"],
        reverse=True
    )

    names = [
        clean_name(doc["file_name"])
        for doc in documents
    ]

    suggestions = []

    # Always available
    suggestions.append("📄 Summarize all uploaded documents.")

    # One document
    if len(names) == 1:
        suggestions.append(f"📚 Explain the main concepts in {names[0]}.")
        suggestions.append(f"🧠 Give a detailed overview of {names[0]}.")
        suggestions.append("🔍 What are the key topics covered?")

    # Two documents
    elif len(names) == 2:
        suggestions.append(f"🔍 Compare {names[0]} and {names[1]}.")
        suggestions.append(f"📚 Explain the concepts in {names[0]}.")
        suggestions.append(f"📚 Explain the concepts in {names[1]}.")

    # Three or more documents
    else:
        suggestions.append(
            f"🔍 Compare {names[0]} and {names[1]}."
        )

        suggestions.append(
            f"📚 Explain the concepts in {names[2]}."
        )

        suggestions.append(
            "🧠 Compare information across all uploaded documents."
        )

    return suggestions

def stream_text(text: str):
    """
    Simulates streaming by yielding one word at a time.
    """

    for word in text.split():
        yield word + " "
        time.sleep(0.03)

repository = get_documents()

has_documents = (
    repository["success"] and
    repository["data"]["total_documents"] > 0
)

suggestions = []

if has_documents:
    suggestions = generate_suggestions(
        repository["data"]["documents"]
    )

if "messages" not in st.session_state:
    # checks if the st.session_state dictionary contains any key "messages"
    # if not then initialize it for new chats else if it is been initialized
    # and chat is going on then skip it.

    st.session_state.messages = []

question = None

if not st.session_state.messages:
    if not has_documents:

        st.info(
             "📂 Your knowledge base is currently empty."
        )

        st.markdown("""
        Upload one or more industrial documents from the **Upload Documents** page to:

        - 📄 Build your knowledge base
        - 🔍 Perform semantic search
        - 🤖 Ask AI-powered questions
        - 📚 View retrieved source citations
        """)

    else:

        st.info(
            "👋 Start by asking a question about your indexed documents."
        )

        st.markdown("### 💡 Suggested Questions")

        cols = st.columns(2)

        for i, suggestion in enumerate(suggestions):

            with cols[i % 2]:

                if st.button(
                    suggestion,
                    use_container_width=True,
                    key=f"suggestion_{i}"
                ):
                    question = suggestion

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            sources = message.get("sources",[])

            if sources:
                st.markdown("#### 📚 Retrieved Sources")

                grouped_sources = {}

                # Group sources by file name
                for source in sources:
                    file_name = source["metadata"]["file_name"]

                    if file_name not in grouped_sources:
                        grouped_sources[file_name] = []

                    grouped_sources[file_name].append(source)

                for document_sources in grouped_sources.values():
                    document_sources.sort(key=lambda source: source["distance"])

                sorted_documents = sorted(
                    grouped_sources.items(),
                    key=lambda item: min(source["distance"] for source in item[1])
                )

                # Display grouped citations
                for file_name, document_sources in sorted_documents:

                    best_relevance = (1 - document_sources[0]["distance"]) * 100

                    st.markdown(
                        f"##### 📄 {file_name} &nbsp;&nbsp; ⭐ Best Retrieved Chunk: {best_relevance:.1f}%"
                    )

                    for source in document_sources:
                        metadata = source["metadata"]

                        with st.expander(
                                f"Chunk {metadata['chunk_id']}"
                        ):
                            relevance = (1 - source["distance"]) * 100

                            st.caption(f"Relevance Score: {relevance:.1f}%")

                            st.write(source["text"])



typed_question = st.chat_input(
    "Ask a question about your documents...",
       disabled=not has_documents
)

if typed_question:
    question = typed_question

if question:
    st.session_state.messages.append(
                                    {  "role": "user",
                                       "content": question
                                    }
                                )
    with st.chat_message("user"):
        st.markdown(question)

    with st.spinner("Generating response..."):
        result = ask_question(question)

    if result["success"]:
        response = result["data"]

        with st.chat_message("assistant"):

            streamed_answer = st.write_stream(
                stream_text(response["answer"])
            )

        st.session_state.messages.append(
            {"role": "assistant",
             "content": streamed_answer,
             "sources": response.get("sources", [])
             }
        )
    else:
        st.session_state.messages.append(
            {"role": "assistant",
             "content": f" ❌ {result['error']}"}
        )
    st.rerun()


