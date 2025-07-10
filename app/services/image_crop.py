from PIL import Image
import os

def crop_image(filepath: str, top: int = 500, bottom: int = 580) -> bool:
    """
    Crop ảnh: cắt bỏ top px phía trên và bottom px phía dưới.
    Nếu ảnh quá nhỏ (cropHeight <= 0) thì giữ nguyên ảnh gốc.
    Ảnh crop sẽ ghi đè lên ảnh gốc.
    """
    try:
        with Image.open(filepath) as img:
            width, height = img.size
            crop_height = height - top - bottom
            if crop_height <= 0:
                # Ảnh quá nhỏ, không crop
                print(f"[CROP] Ảnh quá nhỏ, giữ nguyên: {filepath}")
                return False
            cropped = img.crop((0, top, width, top + crop_height))
            cropped.save(filepath)
            print(f"[CROP] Đã crop và ghi đè ảnh: {filepath}")
            return True
    except Exception as e:
        print(f"[CROP ERROR] {e}")
        return False
