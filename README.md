# QC Agent Skill

## 1. Giới thiệu

QC Agent Skill là một hệ thống tự động hóa quy trình kiểm thử phần mềm, được thiết kế để hỗ trợ các kỹ sư QC/QA trong việc quản lý và thực thi kiểm thử. Hệ thống này tích hợp khả năng đọc hiểu yêu cầu, phân tích logic nghiệp vụ, tạo test case, ghi nhận lỗi (bug tracking), và tự động hóa báo cáo.

## 2. Tính năng chính

### 2.1. Quản lý Test Case thông minh
- **Phân tích yêu cầu:** Tự động đọc và phân tích các file yêu cầu (logic, spec) để trích xuất thông tin cần thiết.
- **Tạo Test Case:** Sinh ra các Test Case chi tiết bao gồm: ID, Tiêu đề, Loại (Positive/Negative), Điều kiện tiên quyết, Các bước thực hiện và Kết quả mong đợi.
- **Đồng bộ Google Sheets:** Tự động ghi nhận Test Case lên Google Sheets để quản lý tập trung.

### 2.2. Quản lý Bug Tracking
- **Ghi nhận lỗi:** Ghi lại thông tin lỗi (Defect) bao gồm: Mô tả, Mức độ nghiêm trọng, Ưu tiên, Ảnh chụp màn hình, và các thông tin liên quan.
- **Tự động hóa báo cáo:** Tự động tạo báo cáo tổng hợp (Excel & Charts) dựa trên dữ liệu lỗi.
- **Đồng bộ Google Sheets:** Đồng bộ dữ liệu lỗi lên Google Sheets để theo dõi tiến độ.

### 2.3. Báo cáo và Thống kê
- **Biểu đồ trực quan:** Tự động tạo các biểu đồ (Pie Chart, Bar Chart) để phân tích tỷ lệ lỗi theo Module, Mức độ nghiêm trọng, và Trạng thái.
- **Báo cáo Excel:** Xuất báo cáo chi tiết ra file Excel để lưu trữ và chia sẻ.

## 3. Cài đặt và Sử dụng

### 3.1. Yêu cầu môi trường
- Python 3.8 trở lên
- Các thư viện: `pandas`, `gspread`, `matplotlib`, `google-auth-oauthlib`, `google-auth-httplib2`

### 3.2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 3.3. Cấu hình Google Sheets
1. Tạo Service Account trên Google Cloud Console.
2. Tải file `credentials.json` và đặt vào thư mục gốc của dự án.
3. Cập nhật email của bạn trong file `sheet_logger.py` để nhận quyền truy cập.

### 3.4. Hướng dẫn sử dụng

**Bước 1: Chuẩn bị dữ liệu đầu vào**
Đặt file yêu cầu (logic/spec) vào thư mục `assets/project/inputs/`.

**Bước 2: Chạy Agent**
```bash
python main.py --project <tên_dự_án>
```

**Bước 3: Kiểm tra kết quả**
- Kết quả Test Case và Bug sẽ được lưu tại `assets/<tên_dự_án>/`.
- Báo cáo biểu đồ sẽ được lưu tại `assets/<tên_dự_án>/outputs/`.
- Dữ liệu cũng được đồng bộ lên Google Sheets tương ứng với tên dự án.

## 4. Cấu trúc dự án
```
QC_Agent_Skill/
├── assets/
│   ├── project/
│   │   ├── inputs/          # File yêu cầu đầu vào
│   │   ├── outputs/         # File báo cáo và biểu đồ
│   │   ├── bug_tracking_db.xlsx # Database lỗi
│   │   └── testcase_db.xlsx   # Database test case
├── references/
│   ├── project/
│   │   ├── bug_guidelines.md  # Hướng dẫn viết bug
│   │   └── testcase_template.md # Template test case
├── scripts/
│   ├── log_manager.py       # Quản lý ghi log
│   ├── generate_reports.py  # Tạo báo cáo
│   ├── read_requirements.py # Đọc và phân tích yêu cầu
│   └── sheet_logger.py      # Ghi log vào Google Sheets
├── SKILL.md                 # Mô tả kỹ năng
├── requirements.txt         # Danh sách thư viện
└── README.md                # Tài liệu này
```

## 5. Ghi chú
- Hệ thống sử dụng Service Account để truy cập Google Sheets, đảm bảo an toàn và bảo mật.
- Các file Excel cục bộ được sử dụng làm bản sao lưu (backup) và nguồn dữ liệu chính cho việc tạo báo cáo.
