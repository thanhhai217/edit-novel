# edit-novel

Web app Python (FastAPI backend, frontend đơn giản) tự động biên tập truyện convert từ tiếng Trung sang tiếng Việt.

## Chức năng chính
- Crawl chương bằng Selenium (hỗ trợ login bằng cookies)
- Screenshot và crop ảnh chương
- OCR tiếng Việt bằng Tesseract
- Gửi nội dung cho AI (OpenAI/Claude/Gemini) để biên tập lại
- Cập nhật kết quả qua API webhook
- Thông báo tiến trình qua Telegram
- Giao diện web: form nhập thông tin, progress bar, log realtime

## Yêu cầu
- Python 3.10+
- Tesseract OCR (cài đặt tại: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract))
- Chrome & ChromeDriver (tương thích version)
- Đặt file `.env` và `cookies.json` ở thư mục gốc

## Cấu trúc dự án
- `app/` : Backend FastAPI (services, routes, logic)
- `templates/` : Giao diện HTML
- `static/` : JS, CSS frontend
- `novel-output-file/` : Lưu file txt và ảnh kết quả
- `.env` : Thông tin API key, Telegram, v.v.
- `cookies.json` : Cookie đăng nhập web truyện

## Hướng dẫn chạy dự án

1. **Tạo môi trường ảo và cài đặt thư viện**
python -m venv .venv .venv\Scripts\activate pip install -r requirements.txt

2. **Cài đặt Tesseract OCR**
- Tải và cài đặt Tesseract (Windows: C:\Program Files\Tesseract-OCR\tesseract.exe)
- Đảm bảo đã cài gói ngôn ngữ tiếng Việt (`vie.traineddata`)

3. **Cài đặt Chrome & ChromeDriver**
- Đảm bảo ChromeDriver phù hợp với phiên bản Chrome

4. **Đặt file cấu hình**
- `.env` (API key, Telegram, v.v.)
- `cookies.json` (cookie đăng nhập web truyện)

5. **Chạy server FastAPI**
uvicorn app.main:app --reload

6. **Truy cập giao diện web**
- Mở trình duyệt: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

7. **Sử dụng web app**
- Nhập URL truyện, chương bắt đầu/kết thúc, nhấn "Bắt đầu" để chạy pipeline tự động

## Lưu ý
- Không commit `.env`, `cookies.json`, `novel-output-file/` lên GitHub (đã có trong `.gitignore`)
- Nếu gặp lỗi thiếu thư viện, chạy lại: `pip install -r requirements.txt`
- Nếu gặp lỗi Tesseract, kiểm tra lại đường dẫn và cài đặt ngôn ngữ


