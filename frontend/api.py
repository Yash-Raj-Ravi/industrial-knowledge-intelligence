# It lets Frontend communicate with Backend
from asyncio import timeout
from pathlib import Path
import requests
from config import BACKEND_URL, REQUEST_TIMEOUT, UPLOAD_ENDPOINT, EMBED_ENDPOINT, ASK_ENDPOINT, EXTRACT_ENTITIES_ENDPOINT


def get_url(endpoint:str) -> str:
    return f"{BACKEND_URL}{endpoint}"

# Check if the backend API is reachable
def check_backend() -> bool:
    """
       Checks whether the backend API is reachable and healthy.

       Returns:
           bool: True if backend is online, otherwise False.
       """


    try:
            response = requests.get(
                get_url("/"),
                timeout=REQUEST_TIMEOUT
            )
            if response.status_code != 200:
                return False
            data = response.json()

            return data.get("status") == "success"
    except requests.RequestException:
            return False

def upload_document(uploaded_file) -> dict:
    """
    Uploads a document to the backend and indexes it.

    Returns:
        dict: {
            "success": bool,
            "data": dict | None,
            "error": str | None
        }
    """
    try:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        upload_response = requests.post(
            get_url(UPLOAD_ENDPOINT),
            files=files,
            timeout=REQUEST_TIMEOUT
        )

        if upload_response.status_code != 200:
            return {
                "success": False,
                "error": upload_response.json().get(
                    "detail",
                    "Failed to upload document."
                )
            }

        upload_data = upload_response.json()
        file_path = Path(upload_data["path"])

        embed_response = requests.post(
            get_url(EMBED_ENDPOINT),
            json={
                "file_path": str(file_path)
            },
            timeout=REQUEST_TIMEOUT
        )
        # print("Status:", embed_response.status_code)
        # print("Body:", embed_response.text)

        if embed_response.status_code != 200:
            return {
                "success": False,
                "error": embed_response.json().get(
                    "detail",
                    "Failed to index document."
                )
            }

        return {
            "success": True,
            "data": embed_response.json()
        }

    except requests.RequestException:
        return {
            "success": False,
            "error": "Unable to connect to the backend."
        }
def extract_entities(document_id: str) -> dict:
    try:
        response = requests.post(
            get_url(EXTRACT_ENTITIES_ENDPOINT),
            json={"document_id": document_id},
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code != 200:
            return {
                "success": False,
                "error": response.json().get(
                    "detail",
                    "Failed to extract entities."
                )
            }

        return {
            "success": True,
            "data": response.json()
        }

    except requests.RequestException:
        return {
            "success": False,
            "error": "Unable to connect to backend."
        }

def ask_question(question:str) -> dict:
    """
    Sends a question to the RAG backend.

    Returns:
        dict: {
            "success": bool,
            "data": dict | None,
            "error": str | None
        }
    """
    try:
        ask_response = requests.post(
            get_url(ASK_ENDPOINT),
            json={
                "query" : question,
                "top_k" : 20,
                "include_sources" : True
                },
            timeout = REQUEST_TIMEOUT
        )
        if ask_response.status_code != 200:
            return {"success": False,
                    "error": ask_response.json().get("detail", "Failed to retrieve an answer.")}

        return {"success": True, "data": ask_response.json()}

    except requests.RequestException:
        return {
            "success": False,
            "error": "Unable to connect to the backend."
        }

def get_documents() -> dict:
    try:
        response = requests.get(
            get_url("/documents"),
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code != 200:
            return {
                "success": False,
                "error": response.json().get(
                    "detail",
                    "Failed to fetch repository."
                )
            }

        return {
            "success": True,
            "data": response.json()
        }

    except requests.RequestException:
        return {
            "success": False,
            "error": "Unable to connect to backend."
        }

def reset_database() -> dict:
    try:
        response = requests.post(
            get_url("/reset"),
            timeout=REQUEST_TIMEOUT
        )
        if response.status_code != 200:
            return {
                "success": False,
                "error": response.json().get(
                    "detail",
                    "Failed to reset database."
                )
            }

        return {
            "success": True,
            "data": response.json()
        }

    except requests.RequestException:
        return {
            "success": False,
            "error": "Unable to connect to backend."
        }

def delete_document(document_id: str) -> dict:
    try:
        response = requests.delete(
            get_url(f"/documents/{document_id}"),
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code != 200:
            return {
                "success": False,
                "error": response.json().get(
                    "detail",
                    "Failed to delete document."
                )
            }

        return {
            "success": True,
            "data": response.json()
        }

    except requests.RequestException:
        return {
            "success": False,
            "error": "Unable to connect to backend."
        }


