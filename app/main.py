
from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path

import os
import shutil
from app.services.chapter_screenshot import get_chapter_urls, screenshot_chapter


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# Serve index.html
@app.get("/", response_class=HTMLResponse)
def index():
    html = (Path(__file__).parent.parent / "templates" / "index.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)

# API nhận dữ liệu form và lưu file txt, ảnh demo
@app.post("/process")
async def process_novel(
    request: Request,
    novel_url: str = Form(...),
    start_chapter: int = Form(...),
    end_chapter: int = Form(...)
):
    # Tạo thư mục output nếu chưa có
    output_dir = Path(__file__).parent.parent / "novel-output-file"
    output_dir.mkdir(exist_ok=True)
    # Lưu file txt theo cấu trúc url chương
    from urllib.parse import urlparse
    base_url = novel_url.rstrip('/')
    txt_files = []
    chapter_urls = get_chapter_urls(novel_url, start_chapter, end_chapter)
    txt_files = []
    img_files = []
    cookies_path = Path(__file__).parent.parent / "cookies.json"
    from app.services.telegram_notify import send_telegram_message
    batch_log = []
    for chapter_url in chapter_urls:
        from urllib.parse import urlparse
        parsed = urlparse(chapter_url)
        rel_path = parsed.path.strip('/').replace('/', '-')
        txt_file_path = output_dir / (rel_path + ".txt")
        img_file_path = output_dir / (rel_path + ".png")
        try:
            print(f"[START] {chapter_url}")
            info = screenshot_chapter(chapter_url, str(cookies_path), img_file_path)
            print(f"[SCREENSHOT] {img_file_path}")
            from app.services.image_crop import crop_image
            crop_image(str(img_file_path), top=500, bottom=580)
            print(f"[CROP] {img_file_path}")
            img_files.append(str(img_file_path))
            from app.services.ocr import ocr_image
            ocr_text = ocr_image(str(img_file_path), lang='vie')
            print(f"[OCR] {chapter_url} => {len(ocr_text)} chars")
            from app.services.gemini_edit import edit_with_gemini
            edited_text = edit_with_gemini(ocr_text)
            print(f"[GEMINI] Done editing {chapter_url}")
            novel_name = info.get("novel_name", "")
            chapter_title = info.get("chapter_title", "")
            import re
            match = re.search(r"/chuong-(\d+)", chapter_url)
            chapter_no = match.group(1) if match else ""
            # Lọc bỏ dòng giới thiệu không mong muốn từ Gemini
            unwanted = "Tuyệt vời! Dưới đây là bản biên tập lại của chương truyện, đã cố gắng tối ưu để câu từ mượt mà, tự nhiên và phù hợp với thể loại võ hiệp"
            content_clean = edited_text.strip()
            if content_clean.startswith(unwanted):
                content_clean = content_clean[len(unwanted):].lstrip('\n').lstrip()
            txt_content = f"novel_name: {novel_name}\nchapter_title: {chapter_title}\nchapter_no: {chapter_no}\nchapter_url: {chapter_url}\n\ntranslated_content: {content_clean}\n"
            txt_file_path.write_text(txt_content, encoding="utf-8")
            txt_files.append(str(txt_file_path))
            # Gửi kết quả lên API update database
            from app.services.api_update import update_novel_content
            api_ok = update_novel_content(
                novel_name=novel_name,
                title=chapter_title,
                chapter_no=chapter_no,
                novel_url=novel_url,
                chapter_url=chapter_url,
                translated_content=content_clean
            )
            log_msg = f"✅ {chapter_title} (Chương {chapter_no}) đã biên tập xong. File: {txt_file_path}. Update API: {'OK' if api_ok else 'FAIL'}"
            print(log_msg)
            batch_log.append(log_msg)
            send_telegram_message(log_msg)
        except Exception as e:
            err_msg = f"[PROCESS ERROR] {chapter_url}: {e}"
            print(err_msg)
            batch_log.append(err_msg)
            send_telegram_message(err_msg)
    # Gửi tổng kết batch
    send_telegram_message(f"Batch hoàn thành: {len(chapter_urls)} chương.\n" + "\n".join(batch_log))
    # Trả về kết quả
    return JSONResponse({"status": "ok", "txt_files": txt_files, "img_files": img_files})
