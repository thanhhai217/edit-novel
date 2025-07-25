import pytesseract
from PIL import Image
import os

# Thiết lập đường dẫn Tesseract và tessdata
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
TESSDATA_PATH = r'C:\Program Files\Tesseract-OCR\tessdata'

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
os.environ['TESSDATA_PREFIX'] = TESSDATA_PATH

print("Initializing TesseractEngine...")
print(f"Using Tesseract at: {TESSERACT_PATH}")
print(f"Using tessdata at: {TESSDATA_PATH}")

OCR_CONFIG = '--psm 6 --oem 3'


def ocr_image(image_path: str, lang: str = 'vie') -> str:
    """
    Nhận diện text tiếng Việt từ ảnh bằng Tesseract.
    """
    print(f"[OCR] Bắt đầu OCR ảnh: {image_path}")
    print(f"[OCR] Ngôn ngữ: {lang}, Config: {OCR_CONFIG}")
    try:
        with Image.open(image_path) as img:
            text = pytesseract.image_to_string(img, lang=lang, config=OCR_CONFIG)
        print(f"[OCR] Đã hoàn thành OCR, độ dài text: {len(text)} ký tự")
        return text
    except Exception as e:
        print(f"[OCR ERROR] {e}")
        return ""
