from pathlib import Path
import streamlit as st
from api import upload_document

st.title("📄 Upload Documents")

st.caption(
    "Upload industrial documents to index them into the knowledge base for semantic search and AI-powered question answering."
)

uploaded_file = st.file_uploader(
    label="Choose an industrial document",
    type = [
        "pdf",
        "txt",
        "csv",
        "pptx",
        "docx",
        "xlsx"
    ]
)

if uploaded_file is not None:
    st.markdown("### Selected File")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Filename", uploaded_file.name)
    with col2:
        size_mb = uploaded_file.size/(1024*1024)
        st.metric("File Size", f"{size_mb:.2f} MB")
    with col3:
        file_type = Path(uploaded_file.name).suffix[1:].upper()
        st.metric("Type", file_type)

    if st.button("⬆️ Upload File",use_container_width = True):
        with st.spinner("Uploading and indexing document..."):
            result = upload_document(uploaded_file)
        if result["success"]:
            st.success(f"✅ '{uploaded_file.name}' indexed successfully!")
            data = result["data"]
            st.info(
                f"""
                **Chunks Created:** {data['total_chunks']}
                
                **Embedding Dimension:** {data['embedding_dimension']}
                """
            )
        else:
            st.error(result["error"])


