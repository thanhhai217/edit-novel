import requests

def update_novel_content(
    novel_name: str,
    title: str,
    chapter_no: str,
    novel_url: str,
    chapter_url: str,
    translated_content: str,
    api_url: str = "https://n8n.canyou.click/webhook/novel_define_content"
) -> bool:
    """
    Gửi nội dung chương đã biên tập lên API hệ thống.
    Trả về True nếu thành công, False nếu lỗi.
    """
    print(f"[API] Đang cập nhật nội dung chương: {title} (Chương {chapter_no})")
    payload = {
        "novel_name": novel_name,
        "title": title,
        "chapter_no": chapter_no,
        "novel_url": novel_url,
        "chapter_url": chapter_url,
        "translated_content": translated_content
    }
    try:
        print(f"[API] Đang gửi yêu cầu đến: {api_url}")
        response = requests.post(api_url, json=payload, timeout=15)
        response.raise_for_status()
        print(f"[API] Cập nhật thành công")
        return True
    except requests.RequestException as e:
        print(f"[API ERROR] {e}")
        return False
