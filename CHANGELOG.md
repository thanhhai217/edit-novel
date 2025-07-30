# Changelog

Tất cả các thay đổi quan trọng của dự án sẽ được ghi lại trong file này.

Dự án tuân theo [Semantic Versioning](https://semver.org/lang/vi/).

## [Unreleased]

## [1.0.0] - 2025-07-30

### Added
- Phiên bản đầu tiên của ứng dụng chỉnh sửa tiểu thuyết
- Tích hợp Google Gemini API để chỉnh sửa nội dung
- Hỗ trợ OCR để nhận diện văn bản từ ảnh chụp chương truyện
- Giao diện web với HTML/CSS/JavaScript
- API endpoints để cập nhật nội dung
- Tích hợp Telegram để thông báo khi hoàn thành chỉnh sửa
- Chức năng cắt ảnh tự động
- Hỗ trợ xử lý nhiều chương trong tiểu thuyết
- Lưu trữ kết quả đầu ra trong thư mục riêng biệt

### Technical Features
- Backend Python với FastAPI
- Xử lý ảnh với Pillow
- Nhận diện văn bản với pytesseract
- Giao tiếp với Google Gemini API
- Webhook Telegram
- Cấu trúc modular với các service riêng biệt

### Infrastructure
- Cấu trúc thư mục rõ ràng với app/, static/, templates/
- Hỗ trợ biến môi trường qua file .env
- Tích hợp GitHub Actions (CI/CD)
- Documentation trong README.md

## Template cho các phiên bản tiếp theo:

### [X.Y.Z] - YYYY-MM-DD

### Added
- Các tính năng mới

### Changed
- Thay đổi trong các tính năng hiện có

### Deprecated
- Các tính năng sắp bị loại bỏ

### Removed
- Các tính năng đã bị loại bỏ

### Fixed
- Các lỗi đã được sửa

### Security
- Các cập nhật bảo mật

---

**Ghi chú:** Khi release phiên bản mới, cần:
1. Cập nhật version trong file này
2. Thêm mục mới với ngày tháng cụ thể
3. Di chuyển các thay đổi từ "Unreleased" sang mục version mới
4. Commit với message rõ ràng: "Release version X.Y.Z"
