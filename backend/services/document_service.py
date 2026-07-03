import os # used to extract file extension

from ..parsers.parser_factory import get_parser

def parse_document(file_path: str) -> str:
    _, extension = os.path.splitext(file_path)
    # os.path.splitext splits the file into 2 parts 1.File name, 2.Extension
    # we use _, to skip file name and only extract the extension.
    extension = extension.lower() # Convert extracted extensions to lowercase since the Parsers dictionary contain extensions in lowercase
    parser = get_parser(extension) # For pdf file extension extracted above will be .pdf which when passed to get_parser returns parse_pdf thus parser = parse_pdf
    text = parser(file_path)
    return text

