from backend.config import TESSERACT_PATH
from PIL import Image
import pytesseract


class OCRService:

    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = str(TESSERACT_PATH)

    def extract_text(self, image: Image.Image) -> str:
        return pytesseract.image_to_string(image)