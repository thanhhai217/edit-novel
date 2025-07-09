# edit-novel

Web app Python (FastAPI backend, frontend đơn giản) tự động biên tập truyện convert từ tiếng Trung sang tiếng Việt.

## Chức năng chính
- Crawl chương bằng Selenium
- OCR bằng Tesseract
- Gửi nội dung cho AI (OpenAI/Claude/Gemini)
- Cập nhật kết quả qua API
- Thông báo tiến trình qua Telegram
- Giao diện web: form nhập thông tin, progress bar, log realtime

## Hướng dẫn khởi động (sẽ bổ sung sau khi scaffold project)

## Yêu cầu
- Python 3.10+
- Tesseract OCR
- Chrome/Chromedriver

## Cấu trúc sẽ gồm:
- Backend: FastAPI
- Frontend: HTML/JS đơn giản (có thể dùng Jinja2 hoặc React/Vue nếu muốn mở rộng)
- Thư mục scripts, static, templates
