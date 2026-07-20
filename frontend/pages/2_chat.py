import streamlit as st
from api import ask_question, get_documents
from components.sidebar import render_sidebar
from pathlib import Path
import time
from datetime import datetime
from utils.chat_export import generate_chat_markdown

render_sidebar()


if "messages" not in st.session_state:
    # checks if the st.session_state dictionary contains any key "messages"
    # if not then initialize it for new chats else if it is been initialized
    # and chat is going on then skip it.

    st.session_state.messages = []

col1, col2 = st.columns([5,1])

with col1:
    st.title("💬 Chat with Knowledge Base")

with col2:
    if st.session_state.messages:
        markdown = generate_chat_markdown(
            st.session_state.messages
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")

        st.download_button(
            "📥 Export",
            markdown,
            file_name=f"chat_history_{timestamp}.md",
            mime="text/markdown"
        )

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

def display_sources(sources):
    """
    Displays retrieved source citations grouped by document.
    """

    if not sources:
        return

    st.markdown("#### 📚 Retrieved Sources")

    grouped_sources = {}

    # Group sources by file name
    for source in sources:
        file_name = source["metadata"]["file_name"]

        if file_name not in grouped_sources:
            grouped_sources[file_name] = []

        grouped_sources[file_name].append(source)

    # Sort chunks within each document
    for document_sources in grouped_sources.values():
        document_sources.sort(
            key=lambda source: source["distance"]
        )

    # Sort documents by best matching chunk
    sorted_documents = sorted(
        grouped_sources.items(),
        key=lambda item: min(
            source["distance"] for source in item[1]
        )
    )

    # Display grouped citations
    for file_name, document_sources in sorted_documents:

        st.markdown(
            f"##### 📄 {file_name} &nbsp;&nbsp; ⭐ Best Matching Chunk"
        )

        for source in document_sources:
            metadata = source["metadata"]

            with st.expander(
                f"Chunk {metadata['chunk_id']}"
            ):
                st.caption(
                    f"Chunk {metadata['chunk_id']}"
                )
                st.write(source["text"])

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
            confidence = message.get("confidence")

            if confidence is not None:
                if confidence >= 85:
                    st.success(
                        f"🟢 Answer Confidence: {confidence:.1f}%"
                    )
                elif confidence >= 60:
                    st.warning(
                        f"🟡 Answer Confidence: {confidence:.1f}%"
                    )
                else:
                    st.error(
                        f"🔴 Answer Confidence: {confidence:.1f}%"
                    )

            display_sources(
                message.get("sources", [])
            )


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

            confidence = response.get("confidence")

            display_sources(
                response.get("sources", [])
            )



            if confidence is not None:
                if confidence >= 85:
                    st.success(
                        f"🟢 Knowledge Retrieval Confidence: {confidence:.1f}%"
                    )
                elif confidence >= 60:
                    st.warning(
                        f"🟡 Knowledge Retrieval Confidence: {confidence:.1f}%"
                    )
                else:
                    st.error(
                        f"🔴 Knowledge Retrieval Confidence: {confidence:.1f}%"
                    )
        st.session_state.messages.append(
            {"role": "assistant",
             "content": streamed_answer,
             "confidence": response.get("confidence"),
             "sources": response.get("sources", [])
             }
        )
    else:
        st.session_state.messages.append(
            {"role": "assistant",
             "content": f" ❌ {result['error']}"}
        )
    st.rerun()


