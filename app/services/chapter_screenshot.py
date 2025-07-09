import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time
from pathlib import Path
from bs4 import BeautifulSoup

def load_cookies(driver, cookies_path):
    with open(cookies_path, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)

def get_chapter_urls(novel_url: str, start_chapter: int, end_chapter: int) -> list:
    """
    Sinh danh sách url chương dựa trên url gốc và số chương.
    """
    urls = []
    for i in range(start_chapter, end_chapter + 1):
        if novel_url.endswith('/'):
            url = f"{novel_url}chuong-{i}"
        else:
            url = f"{novel_url}/chuong-{i}"
        urls.append(url)
    return urls

def screenshot_chapter(url, cookies_path, output_path):
    """
    Dùng selenium + cookies để login, lấy tên truyện, tên chương và chụp toàn bộ trang chương (full page screenshot).
    Trả về dict: {"novel_name": ..., "chapter_title": ...}
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1200,3000')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://metruyencv.com")
    load_cookies(driver, cookies_path)
    driver.get(url)
    time.sleep(2)
    # Lấy chiều cao trang để chụp full page
    scroll_height = driver.execute_script("return document.body.scrollHeight")
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
    # Screenshot
    driver.save_screenshot(str(output_path))
    driver.quit()
    return {"novel_name": novel_name, "chapter_title": chapter_title}

# Ví dụ sử dụng:
# urls = get_chapter_urls(novel_url, start_chapter, end_chapter)
# for idx, url in enumerate(urls, start=start_chapter):
#     screenshot_chapter(url, 'cookies.json', f'novel-output-file/chuong-{idx}.png')
