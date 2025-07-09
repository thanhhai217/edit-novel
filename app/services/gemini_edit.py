import os
import requests

def edit_with_gemini(content: str, prompt_path: str = "prompt.txt") -> str:
    """
    Gửi nội dung cho Gemini (v2.0-flash) để biên tập lại theo prompt.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Chưa cấu hình GEMINI_API_KEY trong .env")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()
    full_prompt = prompt.replace("{content}", content)
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }
    data = {
        "contents": [
            {"parts": [{"text": full_prompt}]}
        ]
    }
    resp = requests.post(url, headers=headers, json=data, timeout=60)
    resp.raise_for_status()
    result = resp.json()
    # Lấy kết quả trả về
    return result["candidates"][0]["content"]["parts"][0]["text"]
