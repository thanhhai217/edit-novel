import os
import requests

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message: str, api_key: str = None, chat_id: str = None) -> bool:
    """
    Gửi thông báo tới Telegram bot.
    """
    api_key = api_key or TELEGRAM_API_KEY
    chat_id = chat_id or TELEGRAM_CHAT_ID
    if not api_key or not chat_id:
        print("[TELEGRAM] Chưa cấu hình API_KEY hoặc CHAT_ID")
        return False

    url = f"https://api.telegram.org/bot{api_key}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"[TELEGRAM ERROR] {e}")
        return False
