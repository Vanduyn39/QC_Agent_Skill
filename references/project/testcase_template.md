# TEMPLATE: CẤU TRÚC TEST CASE (Dành cho AI Agent) - PROJECT A

**[Instruction for AI]:** Khi người dùng yêu cầu tạo Test Case từ một file logic/yêu cầu đầu vào, bạn (AI) PHẢI đọc hiểu logic đó và trích xuất thông tin để tạo Test Case theo đúng định dạng Markdown dưới đây. Không thêm bớt các trường (fields) trừ khi người dùng yêu cầu. Phân tích cả luồng đúng (Happy Path/Positive) và luồng sai (Negative/Edge cases).

---

# 🧪 TEST CASE DOCUMENT: [Tên Tính năng / Module]

## 1. THÔNG TIN CHUNG
* **Tính năng / Module:** [Tên tính năng được phân tích từ file input]
* **Nguồn logic (Reference):** [Tên file input hoặc tóm tắt logic chính]
* **Mục tiêu kiểm thử:** [Mô tả ngắn gọn mục đích của bộ test case này]

---

## 2. TỔNG HỢP TEST CASE (SUMMARY)

| TC ID | Tiêu đề Test Case (Title) | Phân loại | Mức độ ưu tiên (Priority) |
| :--- | :--- | :--- | :--- |
| `TC_001` | [Mô tả ngắn gọn TC 1] | `Positive` / `Negative` | `Urgent` - `Very Low` |
| `TC_002` | [Mô tả ngắn gọn TC 2] | `Positive` / `Negative` | `Urgent` - `Very Low` |
*(AI tự động sinh thêm các dòng tương ứng với số lượng Test Case được tạo)*

---

## 3. CHI TIẾT TEST CASE (DETAILS)

### `TC_001`: [Tiêu đề Test Case - Ví dụ: Đăng nhập thành công với tài khoản hợp lệ]
* **Mục tiêu (Objective):** Kiểm tra xem hệ thống xử lý như thế nào khi [điều kiện test].
* **Loại (Type):** `Positive` / `Negative`
* **Severity (Độ nghiêm trọng):** `Blocking` - `Very Low` (Dựa trên ma trận Defect)
* **Điều kiện tiên quyết (Pre-conditions):**
  * [Điều kiện 1 cần có trước khi test, ví dụ: Tài khoản đã được kích hoạt]
  * [Điều kiện 2]
* **Dữ liệu test (Test Data):**
  * Username: `[Dữ liệu mẫu từ logic]`
  * Password: `[Dữ liệu mẫu từ logic]`
* **Các bước thực hiện (Test Steps):**
  1. [Bước 1: Hành động của người dùng]
  2. [Bước 2: Hành động tiếp theo]
  3. [Bước 3: Nhấp vào nút X/Y/Z]
* **Kết quả mong đợi (Expected Result):**
  * [Hệ thống phải hiển thị thông báo gì?]
  * [Trạng thái database/UI thay đổi ra sao theo đúng file logic input?]

---

### `TC_002`: [Tiêu đề Test Case 2 - Ví dụ: Báo lỗi khi để trống trường bắt buộc]
* **Mục tiêu (Objective):** [Mô tả mục tiêu]
* **Loại (Type):** `Negative`
* **Severity (Độ nghiêm trọng):** `Blocking` - `Very Low`
* **Điều kiện tiên quyết (Pre-conditions):**
  * [Điều kiện...]
* **Dữ liệu test (Test Data):**
  * Field A: `[Trống]`
* **Các bước thực hiện (Test Steps):**
  1. [Bước 1]
  2. [Bước 2]
* **Kết quả mong đợi (Expected Result):**
  * [Mô tả kết quả lỗi dự kiến theo file logic input]

*(AI lặp lại cấu trúc này cho đến khi bao phủ hết toàn bộ logic được cung cấp trong file input)*