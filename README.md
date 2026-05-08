# 🚀 Translate Tools - Ứng dụng Quét và Dịch màn hình

Ứng dụng dịch thuật cá nhân được xây dựng bằng Python, hỗ trợ quét vùng màn hình để nhận diện chữ (OCR) và dịch sang nhiều ngôn ngữ (Anh, Việt, Nhật, Trung).

## ✨ Tính năng
- **Giao diện hiện đại:** Sử dụng CustomTkinter với phong cách bo góc.
- **Quét vùng màn hình:** Chọn một vùng bất kỳ trên màn hình để đọc chữ.
- **Đa ngôn ngữ:** Hỗ trợ nhận diện và dịch giữa Tiếng Anh, Việt, Nhật và Trung Quốc.
- **Tốc độ nhanh:** Sử dụng Google Translate API ổn định.

## 🛠 Yêu cầu hệ thống
1. **Python 3.10+**
2. **Tesseract OCR:** Đây là bộ lõi quan trọng nhất để đọc chữ.
   - Tải bản cài đặt cho Windows tại: [Tesseract OCR Windows](https://github.com/UB-Mannheim/tesseract/wiki)
   - **Lưu ý:** Khi cài đặt, hãy tích chọn thêm gói ngôn ngữ (Additional language data) cho tiếng Nhật và tiếng Trung.
   - Đường dẫn mặc định: `C:\Program Files\Tesseract-OCR\tesseract.exe`

## 🚀 Hướng dẫn cài đặt

1. **Tải mã nguồn về máy:**
   ```bash
   git clone [https://github.com/username/TranslateTools.git](https://github.com/username/TranslateTools.git)
   cd TranslateTools