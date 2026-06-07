# AI 3D Asset Organizer (Python/FastAPI)

Mini web app hỗ trợ quản lý, phân loại và chuẩn hóa dữ liệu bằng AI.

## Yêu cầu môi trường
- Python 3.8 trở lên
- pip (Trình quản lý gói của Python)

## Cài đặt & Chạy Local
1. Clone / Tải source code về máy.
2. Mở terminal tại thư mục dự án và tạo môi trường ảo (khuyến nghị):
   
   python -m venv venv
   source venv/bin/activate  # Trên Windows dùng: venv\Scripts\activate
   
3. Cài đặt các thư viện cần thiết:
   
   pip install -r requirements.txt
  
4. Tạo file `.env` ở thư mục gốc và thêm API Key của Gemini vào có thể lấy miễn phí ở https://aistudio.google.com/app/api-keys:
   
   GEMINI_API_KEY="your_gemini_api_key_here"
   
5. Khởi chạy server:
   python main.py
6. Truy cập ứng dụng tại trình duyệt: http://127.0.0.1:8000