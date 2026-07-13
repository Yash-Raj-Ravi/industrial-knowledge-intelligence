import os # used to extract file extension

from ..core.ocr import OCRService
from ..parsers.parser_factory import get_parser

class DocumentService:
    def __init__(self, ocr_service: OCRService):
        self.ocr_service = ocr_service
    
    def parse_document(self,file_path: str) -> str:
        _, extension = os.path.splitext(file_path)
        # os.path.splitext splits the file into 2 parts 1.File name, 2.Extension
        # we use _, to skip file name and only extract the extension.
        extension = extension.lower() # Convert extracted extensions to lowercase since the Parsers dictionary contain extensions in lowercase
        parser = get_parser(extension) # For pdf file extension extracted above will be .pdf which when passed to get_parser returns parse_pdf thus parser = parse_pdf
        if extension == ".pdf":
            return parser(file_path, self.ocr_service)

        return parser(file_path)


