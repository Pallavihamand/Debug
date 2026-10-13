
import pytesseract
from PIL import Image

# Configure Tesseract OCR on Windows
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text(image_path: str) -> str:
    try:
        with Image.open(image_path) as image:
            return pytesseract.image_to_string(image)
    except Exception as e:
        return f"OCR failed: {str(e)}"
