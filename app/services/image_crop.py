from PIL import Image
import os

def crop_image(filepath: str, top: int = 500, bottom: int = 570) -> bool:
    """
    Crop ảnh: cắt bỏ top px phía trên và bottom px phía dưới.
    Nếu ảnh quá nhỏ (cropHeight <= 0) thì giữ nguyên ảnh gốc.
    Ảnh crop sẽ ghi đè lên ảnh gốc.
    """
    try:
        img = Image.open(filepath)
        width, height = img.size
        crop_top = top
        crop_bottom = bottom
        crop_height = height - crop_top - crop_bottom
        if crop_height <= 0:
            # Ảnh quá nhỏ, không crop
            print(f"[CROP] Ảnh quá nhỏ, giữ nguyên: {filepath}")
            return False
        cropped = img.crop((0, crop_top, width, crop_top + crop_height))
        cropped.save(filepath)
        print(f"[CROP] Đã crop và ghi đè ảnh: {filepath}")
        return True
    except Exception as e:
        print(f"[CROP ERROR] {e}")
        return False
