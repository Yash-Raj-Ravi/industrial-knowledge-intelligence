from PIL import Image

from ..core.ocr import OCRService


def parse_image(file_path: str, ocr_service: OCRService) -> str:
    with Image.open(file_path) as image:
        text = ocr_service.extract_text(image)

        print("=" * 60)
        print("OCR OUTPUT:")
        print(repr(text))
        print("=" * 60)

        return text