from pathlib import Path
import streamlit as st
from api import upload_document
from components.sidebar import render_sidebar
from PIL import Image

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
        "xlsx",
        "png",
        "jpg",
        "jpeg"
    ],
    accept_multiple_files=True
)

camera_image = st.camera_input("📷 Capture a document")

st.caption(
    "📷 For best OCR results: use good lighting, keep the document flat, "
    "fill most of the frame, and avoid blur."
)

uploaded_files = uploaded_files or []

all_files = list(uploaded_files)

if camera_image:
    all_files.append(camera_image)

if all_files:
    st.markdown("### Selected Documents")

    total_size = sum(file.size for file in all_files) / (1024 * 1024)

    st.info(
        f"""
        **Total Files:** {len(all_files)}

        **Total Size:** {total_size:.2f} MB
        """
    )

    for uploaded_file in all_files:

        extension = Path(uploaded_file.name).suffix.lower()

        if extension in [".png", ".jpg", ".jpeg"]:
            image = Image.open(uploaded_file)
            st.image(image, caption=uploaded_file.name, width=300)

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

            for i, uploaded_file in enumerate(all_files):

                result = upload_document(uploaded_file)

                progress.progress((i + 1) / len(all_files))

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