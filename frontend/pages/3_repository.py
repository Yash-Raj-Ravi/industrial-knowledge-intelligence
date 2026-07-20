import streamlit as st
from api import get_documents, reset_database , extract_entities, delete_document
from components.sidebar import render_sidebar

render_sidebar()

@st.dialog("🗑 Delete Document")
def confirm_delete(document_id: str, file_name: str):
    st.warning(
        f"Are you sure you want to delete **{file_name}**?"
    )

    st.caption(
        "This action cannot be undone."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Cancel",
                key=f"cancel_{document_id}",
            use_container_width=True
        ):
            st.rerun()

    with col2:
        if st.button(
            "Delete",
                key=f"confirm_delete_{document_id}",
            type="primary",
            use_container_width=True
        ):
            with st.spinner("Deleting document..."):
                result = delete_document(document_id)

            if result["success"]:
                st.success(result["data"]["message"])
                st.rerun()
            else:
                st.error(result["error"])


st.title("📂 Document Repository")

st.info(
    "Browse all indexed documents currently available in the Industrial Knowledge Base."
)


search_query = st.text_input(
    "🔍 Search Documents",
    placeholder="Search by file name..."
)

result  = get_documents()

if result["success"]:
    data = result["data"]

    col1, col2 = st.columns(2)

    filtered_documents = [
        document
        for document in data["documents"]
        if search_query.lower() in document["file_name"].lower()
    ]

    with col1:
        st.metric(
            "Total Documents",
            len(filtered_documents)
            if search_query
            else data["total_documents"]
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

    if not filtered_documents:
        st.info(
            f'No documents found matching "{search_query}".'
        )

    for document in filtered_documents:


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
            st.divider()

            button_col1, button_col2 = st.columns(2)

            with button_col1:
                    if st.button(
                            "🔍 Extract Entities",
                            key=f"extract_{document['document_id']}",
                            use_container_width=True
                    ):
                        with st.spinner("Extracting entities..."):

                            result = extract_entities(document["document_id"])

                        if result["success"]:

                            entities = result["data"]["entities"]

                            st.success("Entities extracted successfully!")

                            for category, values in entities.items():

                                if not values:
                                    continue

                                with st.expander(
                                        category.replace("_", " ").title(),
                                        expanded=False
                                ):

                                    for value in values:
                                        st.write(f"• {value}")

                        else:
                            st.error(result["error"])

            with button_col2:

                if st.button(
                        "🗑 Delete",
                        key=f"delete_{document['document_id']}",
                        use_container_width=True
                ):
                    confirm_delete(
                        document["document_id"],
                        document["file_name"]
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