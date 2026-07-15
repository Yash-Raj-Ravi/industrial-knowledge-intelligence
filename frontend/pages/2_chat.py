import streamlit as st
from api import ask_question

st.title("💬 Chat with Knowledge Base")

st.caption(
    "Ask questions about your indexed industrial documents using Retrieval-Augmented Generation (RAG)."
)

if "messages" not in st.session_state:
    f"""
    checks if the st.session_state dictionary contains any key "messages" 
    if not then initialize it for new chats else if it is been initialized 
    and chat is going on then skip it.
    """
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question about your documents...")

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
        answer = result["data"]["answer"]
        st.session_state.messages.append(
            {"role": "assistant",
             "content": answer
             }
        )
    else:
        st.session_state.messages.append(
            {"role": "assistant",
             "content": f" ❌ {result['error']}"}
        )
    st.rerun()


