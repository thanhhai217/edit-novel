<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Copilot Instructions for edit-novel

- Đây là dự án Python web app (FastAPI backend, frontend đơn giản) để tự động biên tập truyện convert từ tiếng Trung sang tiếng Việt.
- Yêu cầu: crawl chương bằng Selenium, OCR bằng Tesseract, gửi nội dung cho AI (OpenAI/Claude/Gemini), cập nhật kết quả qua API, thông báo Telegram, giao diện web có form nhập thông tin, progress bar, log realtime.
- Ưu tiên code rõ ràng, dễ bảo trì, tách biệt backend/frontend, hỗ trợ batch chương, dễ mở rộng AI provider.
