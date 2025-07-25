import os
import requests

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message: str, api_key: str = None, chat_id: str = None) -> bool:
    """
    Gửi thông báo tới Telegram bot.
    """
    print(f"[TELEGRAM] Đang gửi thông báo, độ dài message: {len(message)} ký tự")
    api_key = api_key or TELEGRAM_API_KEY
    chat_id = chat_id or TELEGRAM_CHAT_ID
    
    # Check which variable is missing for better error 
    # reporting
    if not api_key and not chat_id:
        print("[TELEGRAM] Chưa cấu hình TELEGRAM_API_KEY và TELEGRAM_CHAT_ID")
        return False
    elif not api_key:
        print("[TELEGRAM] Chưa cấu hình TELEGRAM_API_KEY")
        return False
    elif not chat_id:
        print("[TELEGRAM] Chưa cấu hình TELEGRAM_CHAT_ID")
        return False

    url = f"https://api.telegram.org/bot{api_key}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        print("[TELEGRAM] Đang gửi yêu cầu đến Telegram API...")
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
        print("[TELEGRAM] Gửi thông báo thành công")
        return True
    except requests.RequestException as e:
        print(f"[TELEGRAM ERROR] {e}")
        return False
