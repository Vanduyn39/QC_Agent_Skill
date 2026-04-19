# 🚀 QC Super Agent - Antigravity Automation

**QC Super Agent** là một hệ thống trợ lý AI chạy trên nền tảng Antigravity, được thiết kế để tự động hóa toàn bộ quy trình làm việc của một chuyên viên Kiểm thử Chất lượng (QC): từ việc đọc yêu cầu nghiệp vụ đến việc tạo Test Case, log bug nhanh chóng, và tự động tổng hợp báo cáo hàng ngày/hàng tuần với các biểu đồ trực quan.

## 📌 Các Tính Năng Chính
- **Tạo Test Case Tự Động:** Tự động đọc các file Yêu cầu (`.docx`, `.pdf`, `.xlsx`) **được đặt trong thư mục `inputs`**, sinh ra các Test Case theo định dạng chuẩn và đẩy trực tiếp lên Google Sheets.
- **Log Bug Siêu Tốc:** Trích xuất thông tin lỗi (bug) từ các câu lệnh ngôn ngữ tự nhiên, phân loại Mức độ nghiêm trọng/Độ ưu tiên (Severity/Priority) theo hướng dẫn của dự án và lưu trữ vào cả file Excel ở máy cá nhân (local) lẫn Google Sheets.
- **Báo Cáo Chuyên Nghiệp:**
    - **Báo Cáo Hàng Ngày (Daily Report):** Tổng hợp số lượng bug được log trong một ngày và phân tích các module gặp lỗi.
    - **Báo Cáo Hàng Tuần (Weekly Report):** Cung cấp thống kê về xu hướng bug trong tuần, đi kèm với các biểu đồ trực quan (`.png`).
- **Quản Lý Đa Dự Án:** Tự động phân loại và quản lý dữ liệu dựa trên cấu trúc thư mục `assets/{project_name}`.

---

## 🛠 Hướng dẫn Thiết lập Google Sheets API

Để cho phép Agent ghi dữ liệu lên Cloud, bạn cần cấp cho nó một "chìa khóa" thông qua Google Cloud Console.

### 1. Tạo Dự án và Lấy File Credentials (Thông tin xác thực)
1. Truy cập [Google Cloud Console](https://console.cloud.google.com/).
2. Tạo một Dự án mới (ví dụ: `QC-Automation-Agent`).
3. Điều hướng tới **APIs & Services > Library**: Tìm và **Bật (Enable)** hai API sau:
    - **Google Sheets API**
    - **Google Drive API**
4. Điều hướng tới **Credentials > Create Credentials > Service Account**:
    - Đặt tên cho Service Account và bấm **Create**.
    - Sau khi tạo xong, nhấp vào email của tài khoản đó, chuyển sang tab **Keys > Add Key > Create New Key**.
    - Chọn định dạng **JSON**. File sẽ được tải xuống máy tính của bạn.
5. Đổi tên file vừa tải xuống thành `credentials.json` và đặt nó vào thư mục gốc của kho lưu trữ (repository) này.

### 2. Tạo Sheet và Chia sẻ Quyền truy cập (Bước Quan Trọng)
Để tránh giới hạn lưu trữ của Google (lỗi Quota Exceeded) đối với Service Account, vui lòng làm theo cách sau:
1. Mở file `credentials.json`, tìm và copy dòng có chứa `"client_email": "..."`.
2. Vào Google Drive cá nhân của bạn và tạo một file Google Sheet mới. Đặt tên file trùng khớp chính xác với tên dự án của bạn (ví dụ: `Comana`).
3. Bấm nút **Share** (Chia sẻ) ở góc trên cùng bên phải.
4. Dán email của Service Account (từ bước 1), thiết lập quyền là **Editor** (Người chỉnh sửa), và bấm **Send** (Gửi).
5. Lặp lại quá trình này cho bất kỳ dự án nào khác mà bạn thêm vào.

---

## 🌱 Cách Thêm Một Dự Án Mới
Hệ thống này có khả năng mở rộng rất cao. Nếu bạn muốn sử dụng nó cho một dự án mới, bạn **không cần thay đổi bất kỳ mã code nào**. Chỉ cần làm theo 3 bước đơn giản sau:
1. **Nhân bản Thư mục:** Nhân bản (duplicate) một thư mục dự án hiện có trong cả `assets/` và `references/`.
2. **Đổi tên:** Đổi tên các thư mục vừa nhân bản thành tên dự án mới của bạn (ví dụ: `assets/Project_X` và `references/Project_X`). Thay thế các hướng dẫn cũ bằng các quy tắc của dự án mới.
3. **Tạo Google Sheet mới:** Tạo một file mới trên Google Drive của bạn với tên là `Project_X` và chia sẻ quyền Editor cho email của Service Account (giống như bước 2 trong Hướng dẫn Thiết lập). 

---

## 📂 Cấu trúc Thư mục
```text
QC_Agent_Skill/
├── credentials.json          # File chứa Google API Key (KHÔNG ĐỂ LỘ)
├── SKILL.md                  # Chỉ dẫn "bộ não" cho Agent
├── assets/                   # Lưu trữ dữ liệu cho từng dự án (Comana, Project_X...)
│   └── {project_name}/
│       ├── inputs/           # ⚠️ THẢ FILE REQUIREMENT CỦA BẠN VÀO ĐÂY ĐỂ AI ĐỌC
│       └── outputs/          # Chứa các báo cáo, biểu đồ được tạo ra và các file excel backup
├── references/               # Các hướng dẫn và quy tắc riêng cho từng dự án
│   └── {project_name}/
│       ├── bug_guidelines.md
│       └── testcase_template.md
└── scripts/                  # Mã nguồn Python xử lý logic
    ├── sheet_logger.py       # Đẩy dữ liệu lên Google Sheets
    ├── log_manager.py        # Quản lý logic ghi log Bug/Test Case
    ├── generate_reports.py   # Vẽ biểu đồ và tạo báo cáo
    └── read_requirements.py  # Đọc file requirements
```
