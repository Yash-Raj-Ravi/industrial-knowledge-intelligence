from .pdf_parser import parse_pdf
from .txt_parser import parse_txt
from .csv_parser import parse_csv
from .pptx_parser import parse_pptx
from .docx_parser import parse_docx
from .xlsx_parser import parse_xlsx

from collections.abc import Callable
# Since every parser has the same signature that is def parse_xxx(file_path: str) -> str:
# we can make the return type explicit using Callable:

PARSERS = {
     ".pdf":parse_pdf,
     ".txt":parse_txt,
     ".csv":parse_csv,
     ".pptx":parse_pptx,
     ".docx":parse_docx,
     ".xlsx":parse_xlsx,

} # Dictionary for mapping parsers

def get_parser(extension: str) -> Callable [[str],str]:
    parser = PARSERS.get(extension)

    if parser is None:
       raise ValueError(
         f"Unsupported file type: {extension}"
       )
    return parser 