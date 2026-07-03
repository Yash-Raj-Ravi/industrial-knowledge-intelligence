import fitz

def parse_pdf(file_path: str) -> str:
    pages_text=[]

    with fitz.open(file_path) as document:
        for page in document:
            page_text = page.get_text("text")
            if page_text.strip():
                pages_text.append(page_text)
    return "\n".join(pages_text)
