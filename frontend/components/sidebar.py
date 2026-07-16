import streamlit as st

from api import check_backend
from api import get_documents


def render_sidebar():

    with st.sidebar:

        st.title("🏭 Industrial KI")

        st.caption(
            "AI-powered Industrial Knowledge Platform"
        )

        st.divider()

        if check_backend():
            st.success("🟢 Backend Online")
        else:
            st.error("🔴 Backend Offline")

        result = get_documents()

        if result["success"]:
            data = result["data"]

            st.metric(
                "📄 Documents",
                data["total_documents"]
            )

            st.metric(
                "🧩 Chunks",
                data["total_chunks"]
            )

        st.divider()

        st.caption("Version 1.0")

        st.caption(
            "FastAPI • Streamlit • Ollama • ChromaDB"
        )