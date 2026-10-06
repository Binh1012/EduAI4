# EduAI 4 – Học trắc nghiệm thông minh cho học sinh lớp 4

Gồm 2 phần: `backend/` (FastAPI) và `android/` (Kotlin + Jetpack Compose + MVVM).

## 1. Chạy backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                   # Windows: copy .env.example .env
# sửa SECRET_KEY; điền ANTHROPIC_API_KEY nếu muốn bật trợ giảng AI
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- Lần chạy đầu tự tạo bảng và nạp dữ liệu mẫu (5 môn). Xem API tại http://localhost:8000/docs
- Dùng PostgreSQL: đổi `DATABASE_URL` trong `.env` và `pip install psycopg2-binary`.

## 2. Chạy Android
1. Mở thư mục `android/` bằng Android Studio (Koala trở lên, JDK 17). Chờ Gradle sync (nếu hỏi, dùng Gradle 8.7).
2. Emulator: giữ nguyên `API_BASE_URL = http://10.0.2.2:8000/` (trong `app/build.gradle.kts`).
   Điện thoại thật: đổi thành `http://<IP-máy-tính>:8000/` (cùng mạng Wi-Fi).
3. Bấm Run. Đăng ký tài khoản mới rồi học thử.
4. Tạo APK: Build > Build Bundle(s) / APK(s) > Build APK(s).

## Đã có (Phase 1–3 + một phần Phase 5)
Đăng ký/đăng nhập (JWT), môn → chủ đề → làm bài có phản hồi + giải thích, chấm điểm phía server,
XP/cấp độ/streak/huy hiệu, màn Tiến độ + chủ đề yếu, gợi ý ôn tập (rule-based), chatbot trợ giảng AI
(qua backend, có giới hạn lượt hỏi và prompt an toàn cho trẻ em).

## Chưa có (làm ở các phase sau)
Màn giáo viên/quản trị (CRUD câu hỏi, tạo đề, thống kê lớp), AI tạo câu hỏi, báo cáo AI sau bài,
offline (Room), thông báo, quên mật khẩu, kiểm thử tự động.
