from pathlib import Path
import streamlit as st
from api import upload_document
from components.sidebar import render_sidebar

render_sidebar()

st.title("📄 Upload Documents")

st.caption(
    "Upload industrial documents to index them into the knowledge base for semantic search and AI-powered question answering."
)

uploaded_files = st.file_uploader(
    label="Choose industrial documents",
    type=[
        "pdf",
        "txt",
        "csv",
        "pptx",
        "docx",
        "xlsx"
    ],
    accept_multiple_files=True
)

if uploaded_files:
    st.markdown("### Selected Documents")

    total_size = sum(file.size for file in uploaded_files) / (1024 * 1024)

    st.info(
        f"""
        **Total Files:** {len(uploaded_files)}

        **Total Size:** {total_size:.2f} MB
        """
    )

    for uploaded_file in uploaded_files:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Filename", uploaded_file.name)

        with col2:
            size_mb = uploaded_file.size / (1024 * 1024)
            st.metric("File Size", f"{size_mb:.2f} MB")

        with col3:
            file_type = Path(uploaded_file.name).suffix[1:].upper()
            st.metric("Type", file_type)

        st.divider()

    if st.button("⬆️ Upload & Index Documents", use_container_width=True):

        progress = st.progress(0)

        success_count = 0
        failed_count = 0

        with st.spinner("Uploading and indexing documents..."):

            for i, uploaded_file in enumerate(uploaded_files):

                result = upload_document(uploaded_file)

                progress.progress((i + 1) / len(uploaded_files))

                if result["success"]:
                    success_count += 1

                    data = result["data"]

                    st.success(f"✅ {uploaded_file.name}")

                    st.caption(
                        f"Chunks: {data['total_chunks']} | "
                        f"Embedding Dimension: {data['embedding_dimension']}"
                    )

                else:
                    failed_count += 1
                    st.error(f"❌ {uploaded_file.name}: {result['error']}")

        st.success(
            f"Finished indexing documents.\n\n"
            f"✅ Successful: {success_count}\n\n"
            f"❌ Failed: {failed_count}"
        )