import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def load_cookies(driver, cookies_path):
    """Nạp cookies từ file vào trình duyệt Selenium."""
    with open(cookies_path, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)

def get_chapter_urls(novel_url: str, start_chapter: int, end_chapter: int) -> list:
    """
    Sinh danh sách url chương dựa trên url gốc và số chương.
    """
    urls = []
    base_url = novel_url.rstrip('/')
    print(f"[CHAPTER_URLS] Tạo danh sách URLs từ chương {start_chapter} đến {end_chapter}")
    for i in range(start_chapter, end_chapter + 1):
        url = f"{base_url}/chuong-{i}"
        urls.append(url)
        print(f"[CHAPTER_URLS] Đã thêm: {url}")
    print(f"[CHAPTER_URLS] Tổng cộng {len(urls)} URLs")
    return urls

def screenshot_chapter(url, cookies_path, output_path):
    """
    Dùng selenium + cookies để login, lấy tên truyện, tên chương và chụp toàn bộ trang chương (full page screenshot).
    Trả về dict: {"novel_name": ..., "chapter_title": ...}
    """
    print(f"[SCREENSHOT] Bắt đầu xử lý chapter: {url}")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1200,3000')
    # Disable Google services to fix DEPRECATED_ENDPOINT error
    chrome_options.add_argument('--disable-background-networking')
    chrome_options.add_argument('--disable-background-timer-throttling')
    chrome_options.add_argument('--disable-backgrounding-occluded-windows')
    chrome_options.add_argument('--disable-breakpad')
    chrome_options.add_argument('--disable-client-side-phishing-detection')
    chrome_options.add_argument('--disable-component-update')
    chrome_options.add_argument('--disable-default-apps')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-domain-reliability')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-features=AudioServiceOutOfProcess')
    chrome_options.add_argument('--disable-hang-monitor')
    chrome_options.add_argument('--disable-ipc-flooding-protection')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-offer-store-unmasked-wallet-cards')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-print-preview')
    chrome_options.add_argument('--disable-prompt-on-repost')
    chrome_options.add_argument('--disable-renderer-backgrounding')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-speech-api')
    chrome_options.add_argument('--disable-sync')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--ignore-gpu-blacklist')
    chrome_options.add_argument('--metrics-recording-only')
    chrome_options.add_argument('--mute-audio')
    chrome_options.add_argument('--no-default-browser-check')
    chrome_options.add_argument('--no-first-run')
    chrome_options.add_argument('--no-pings')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--no-zygote')
    chrome_options.add_argument('--password-store=basic')
    chrome_options.add_argument('--use-gl=swiftshader')
    chrome_options.add_argument('--use-mock-keychain')
    driver = webdriver.Chrome(options=chrome_options)
    try:
        print("[SCREENSHOT] Đang tải trang đăng nhập...")
        driver.get("https://metruyencv.com")
        print("[SCREENSHOT] Đang nạp cookies...")
        load_cookies(driver, cookies_path)
        print(f"[SCREENSHOT] Đang tải trang chapter: {url}")
        driver.get(url)
        time.sleep(2)
        # Lấy chiều cao trang để chụp full page
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        print(f"[SCREENSHOT] Chiều cao trang: {scroll_height}px")
        driver.set_window_size(1200, scroll_height)
        time.sleep(0.5)
        # Lấy HTML để parse tên truyện, tên chương
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        # Tên truyện
        novel_name = ""
        h1 = soup.find("h1", class_="text-lg text-center text-balance")
        if h1:
            a = h1.find("a", class_="text-title font-semibold")
            if a:
                novel_name = a.get_text(strip=True)
        # Tên chương
        chapter_title = ""
        h2 = soup.find("h2", class_="text-center text-gray-600 dark:text-gray-400 text-balance")
        if h2:
            chapter_title = h2.get_text(strip=True)
        print(f"[SCREENSHOT] Novel: {novel_name}, Chapter: {chapter_title}")
        # Screenshot
        print(f"[SCREENSHOT] Đang chụp màn hình vào: {output_path}")
        driver.save_screenshot(str(output_path))
        print(f"[SCREENSHOT] Đã hoàn thành chụp màn hình")
        return {"novel_name": novel_name, "chapter_title": chapter_title}
    finally:
        print("[SCREENSHOT] Đang đóng trình duyệt...")
        driver.quit()

# Ví dụ sử dụng:
# urls = get_chapter_urls(novel_url, start_chapter, end_chapter)
# for idx, url in enumerate(urls, start=start_chapter):
#     screenshot_chapter(url, 'cookies.json', f'novel-output-file/chuong-{idx}.png')
