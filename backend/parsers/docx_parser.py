# Docx is similar to PDF parser ,here instead of iterating over pages, we'll iterate over paragraphs.
from docx import Document

def parse_docx(file_path: str) -> str:
    document = Document(file_path)
    paragraphs_text = []
    for paragraph in document.paragraphs:
        paragraph_text = paragraph.text
        if paragraph_text.strip():
            paragraphs_text.append(paragraph_text)
    return "\n".join(paragraphs_text)