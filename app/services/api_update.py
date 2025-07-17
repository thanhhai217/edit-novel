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
    payload = {
        "novel_name": novel_name,
        "title": title,
        "chapter_no": chapter_no,
        "novel_url": novel_url,
        "chapter_url": chapter_url,
        "translated_content": translated_content
    }
    try:
        response = requests.post(api_url, json=payload, timeout=15)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"[API ERROR] {e}")
        return False
