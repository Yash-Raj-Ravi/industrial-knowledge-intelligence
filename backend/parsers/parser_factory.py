from .pdf_parser import parse_pdf
from .txt_parser import parse_txt
from .csv_parser import parse_csv
from .pptx_parser import parse_pptx
from .docx_parser import parse_docx
from .xlsx_parser import parse_xlsx
from .image_parser import parse_image


from collections.abc import Callable
# Returns the parser function associated with the given file extension.
# Some parsers (e.g. PDF and image) also require an OCRService.
# we can make the return type explicit using Callable:

PARSERS = {
     ".pdf":parse_pdf,
     ".txt":parse_txt,
     ".csv":parse_csv,
     ".pptx":parse_pptx,
     ".docx":parse_docx,
     ".xlsx":parse_xlsx,
     ".png": parse_image,
     ".jpg": parse_image,
     ".jpeg": parse_image

} # Dictionary for mapping parsers

def get_parser(extension: str) -> Callable:
    parser = PARSERS.get(extension)

    if parser is None:
       raise ValueError(
         f"Unsupported file type: {extension}"
       )
    return parser 