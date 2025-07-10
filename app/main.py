from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
from pathlib import Path
import os
import shutil
import time
import asyncio
import re
from urllib.parse import urlparse

from app.services.chapter_screenshot import get_chapter_urls, screenshot_chapter
from app.services.image_crop import crop_image
from app.services.ocr import ocr_image
from app.services.gemini_edit import edit_with_gemini
from app.services.api_update import update_novel_content
from app.services.telegram_notify import send_telegram_message

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

@app.post("/process")
async def process_novel(
    request: Request,
    novel_url: str = Form(...),
    start_chapter: int = Form(...),
    end_chapter: int = Form(...)
):
    async def event_stream():
        output_dir = Path(__file__).parent.parent / "novel-output-file"
        processed_dir = output_dir / "processed"
        output_dir.mkdir(exist_ok=True)
        processed_dir.mkdir(exist_ok=True)
        chapter_urls = get_chapter_urls(novel_url, start_chapter, end_chapter)
        cookies_path = Path(__file__).parent.parent / "cookies.json"
        batch_log = []

        for chapter_url in chapter_urls:
            url_parts = urlparse(chapter_url)
            file_base = "-".join(url_parts.path.strip("/").split("/"))
            txt_file_path = output_dir / f"{file_base}.txt"
            img_file_path = output_dir / f"{file_base}.png"

            yield f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [START] {chapter_url}\n"
            start_time = time.time()

            # Screenshot
            try:
                info = screenshot_chapter(chapter_url, str(cookies_path), img_file_path)
                yield f"[SCREENSHOT] {img_file_path}\n"
            except Exception as e:
                yield f"[SCREENSHOT ERROR] {chapter_url}: {e}\n"
                continue

            # Crop image
            try:
                crop_image(str(img_file_path), top=500, bottom=580)
            except Exception as e:
                yield f"[CROP ERROR] {chapter_url}: {e}\n"

            # OCR
            try:
                ocr_text = ocr_image(str(img_file_path), lang='vie')
                yield f"[OCR] {chapter_url} => {len(ocr_text)} chars\n"
            except Exception as e:
                yield f"[OCR ERROR] {chapter_url}: {e}\n"
                ocr_text = ""

            # Gemini AI
            try:
                edited_text = edit_with_gemini(ocr_text)
                yield f"[GEMINI] Done editing {chapter_url}\n"
            except Exception as e:
                yield f"[GEMINI ERROR] {chapter_url}: {e}\n"
                edited_text = ""

            # Extract info
            novel_name = info.get("novel_name", "")
            chapter_title = info.get("chapter_title", "")
            match = re.search(r"/chuong-(\d+)", chapter_url)
            chapter_no = match.group(1) if match else ""

            # Clean Gemini output
            unwanted = "Tuyệt vời! Dưới đây là bản biên tập lại của chương truyện, đã cố gắng tối ưu để câu từ mượt mà, tự nhiên và phù hợp với thể loại võ hiệp"
            content_clean = edited_text.strip()
            if content_clean.startswith(unwanted):
                content_clean = content_clean[len(unwanted):].lstrip('\n').lstrip()

            # Save txt
            txt_content = (
                f"novel_name: {novel_name}\n"
                f"chapter_title: {chapter_title}\n"
                f"chapter_no: {chapter_no}\n"
                f"chapter_url: {chapter_url}\n\n"
                f"translated_content: {content_clean}\n"
            )
            txt_file_path.write_text(txt_content, encoding="utf-8")

            # Update API
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

            # Move files to processed/
            try:
                processed_txt = processed_dir / txt_file_path.name
                processed_img = processed_dir / img_file_path.name
                shutil.move(str(txt_file_path), str(processed_txt))
                shutil.move(str(img_file_path), str(processed_img))
                yield f"[MOVE] Đã chuyển file txt và ảnh vào {processed_dir}\n"
            except Exception as e:
                yield f"[MOVE ERROR] {chapter_url}: {e}\n"

            end_time = time.time()
            elapsed = end_time - start_time
            yield f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [DONE] {chapter_url} | Thời gian xử lý: {elapsed:.2f} giây\n"
        yield "Hoàn thành!\n"
    return StreamingResponse(event_stream(), media_type="text/plain")
