import pytesseract
from PIL import Image
import os

# Thiết lập đường dẫn Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

print("Initializing TesseractEngine...")
print(f"Using Tesseract at: {pytesseract.pytesseract.tesseract_cmd}")
print(f"Using tessdata at: {os.environ['TESSDATA_PREFIX']}")

OCR_CONFIG = '--psm 6 --oem 3'


def ocr_image(image_path: str, lang: str = 'vie') -> str:
    """
    Nhận diện text tiếng Việt từ ảnh bằng Tesseract.
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang=lang, config=OCR_CONFIG)
        return text
    except Exception as e:
        print(f"[OCR ERROR] {e}")
        return ""
