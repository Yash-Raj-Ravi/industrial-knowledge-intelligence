from .pdf_parser import parse_pdf

PARSERS={
    ".pdf":parse_pdf
} # Dictionary for mapping parsers

def get_parser(extension: str):
    parser = PARSERS.get(extension)

    if parser is None:
       raise ValueError(
         f"Unsupported file type:{extension}"
       )
    return parser 