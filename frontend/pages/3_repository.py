import streamlit as st
from api import get_documents, reset_database
from components.sidebar import render_sidebar

render_sidebar()

st.title("📂 Document Repository")

st.info(
    "Browse all indexed documents currently available in the Industrial Knowledge Base."
)


st.caption("View all indexed documents in the knowledge base.")

result  = get_documents()

if result["success"]:
    data = result["data"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Documents",
            data["total_documents"]
        )

    with col2:
        st.metric(
            "Total Chunks",
            data["total_chunks"]
        )

    st.divider()

    icons = {
        ".pdf": "📕",
        ".pptx": "📊",
        ".docx": "📝",
        ".xlsx": "📈",
        ".csv": "📑",
        ".txt": "📃"
    }
    for document in data["documents"]:


        icon = icons.get(document["document_type"], "📄")
        with st.container(border=True):
            st.markdown(f"###{icon} {document['file_name']}")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Type",
                    document["document_type"].replace(".", "").upper()
                )

            with col2:
                st.metric(
                    "Chunks",
                    document["total_chunks"]
                )

else:
    st.error(result["error"])

st.divider()

st.subheader("⚠️ Danger Zone")

st.caption(
    "This will permanently remove all indexed documents from the knowledge base."
)

confirm = st.checkbox(
    "I understand that this action cannot be undone."
)

if st.button(
    "🗑 Reset Knowledge Base",
    type="primary",
    use_container_width=True,
    disabled=not confirm
):

    with st.spinner("Resetting knowledge base..."):
        result = reset_database()

    if result["success"]:
        st.success(result["data"]["message"])
        st.rerun()
    else:
        st.error(result["error"])