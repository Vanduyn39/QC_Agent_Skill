# Tiêu chuẩn Đánh giá Bug - PROJECT A

Tài liệu này quy định các tiêu chí để hệ thống hóa quy trình phân loại, đánh giá mức độ ảnh hưởng và thứ tự ưu tiên xử lý lỗi (Defect) trong dự án.

---

## 1. Phân biệt Bản chất: Severity vs. Priority

| Đặc điểm | **Severity** (Mức độ nghiêm trọng) | **Priority** (Mức độ ưu tiên) |
| :--- | :--- | :--- |
| **Trọng tâm** | Khía cạnh kỹ thuật & vận hành hệ thống. | Khía cạnh kinh doanh, thời gian & nguồn lực. |
| **Câu hỏi chính** | "Lỗi này phá vỡ hệ thống đến mức nào?" | "Cần phải sửa lỗi này nhanh đến mức nào?" |
| **Chủ thể** | **QA / Tester** (Dựa trên spec & hệ thống) | **PO / PM / Lead** (Dựa trên Roadmap & khách hàng) |

---

## 2. DEFECT BY SEVERITY (Mức độ nghiêm trọng)
*Đánh giá dựa trên tác động của lỗi đối với tính năng và khả năng vận hành của phần mềm.*

| Cấp độ | Mô tả chi tiết |
| :--- | :--- |
| **Blocking** | Lỗi làm tê liệt hoàn toàn hệ thống hoặc chức năng chính. Không có cách khắc phục tạm thời (workaround). Ngăn cản việc kiểm thử các phần liên quan. |
| **Important** | Lỗi ảnh hưởng nặng nề đến các tính năng cốt lõi. Người dùng không thể hoàn thành luồng nghiệp vụ chính (Critical Path). |
| **Moderate** | Lỗi gây mất chức năng nhưng có cách xử lý tạm thời (workaround). Ảnh hưởng đến trải nghiệm nhưng không làm gián đoạn hoàn toàn quy trình. |
| **Low** | Lỗi nhỏ về giao diện (UI) hoặc các tính năng phụ, không ảnh hưởng đến logic nghiệp vụ. |
| **Very Low** | Các lỗi cực nhỏ, lỗi chính tả, hoặc các đề xuất cải thiện thẩm mỹ mang tính cá nhân. |

---

## 3. DEFECT BY PRIORITY (Mức độ ưu tiên)
*Đánh giá dựa trên mức độ khẩn cấp cần được sửa chữa.*

| Cấp độ | Thời hạn xử lý dự kiến |
| :--- | :--- |
| **Urgent** | **Sửa ngay lập tức.** Thường xử lý trong vòng vài giờ hoặc trong ngày. Lỗi chặn đứng tiến độ team hoặc gây thiệt hại trực tiếp. |
| **High** | **Ưu tiên cao.** Cần được giải quyết trong Sprint hiện tại hoặc trước kỳ phát hành (Release) kế tiếp. |
| **Normal** | **Xử lý bình thường.** Sắp xếp sửa sau khi các lỗi quan trọng đã hoàn tất. Có thể chờ đến các bản cập nhật định kỳ. |
| **Low** | **Ưu tiên thấp.** Sửa khi có thời gian trống, không ảnh hưởng đến kế hoạch Release chính. |
| **Very Low** | **Cân nhắc sửa.** Thường là các lỗi thẩm mỹ hoặc mong muốn cải tiến (Suggestion) sẽ xử lý khi nguồn lực dư dả. |

---

## 4. Ma trận phân loại (Defect Triage Matrix)

Việc kết hợp Severity và Priority giúp đội ngũ phát triển tối ưu hóa nguồn lực:

* **Severity Cao / Priority Cao:** Hệ thống hỏng nặng + Cần sửa gấp (Ví dụ: Không thể thanh toán trên Production).
* **Severity Cao / Priority Thấp:** Lỗi kỹ thuật nặng nhưng ít gặp (Ví dụ: Crash app trên dòng điện thoại cũ đã ngừng hỗ trợ).
* **Severity Thấp / Priority Cao:** Lỗi nhẹ nhưng ảnh hưởng lớn đến thương hiệu (Ví dụ: Sai logo công ty, sai thông điệp khuyến mãi ở trang chủ).
* **Severity Thấp / Priority Thấp:** Lỗi nhẹ, ít người thấy (Ví dụ: Lỗi chính tả ở trang điều khoản sử dụng).

---

## 5. Loại Bug (Defect Type)

Khi báo cáo lỗi, cần gán nhãn thuộc các nhóm sau:
* **Functional:** Lỗi sai lệch về logic nghiệp vụ, tính năng không chạy đúng spec.
* **UI/UX:** Lỗi giao diện, sai lệch design, trải nghiệm người dùng không mượt mà.
* **Performance:** Lỗi về tốc độ phản hồi, tải chậm, tràn bộ nhớ.
* **Security:** Các lỗ hổng bảo mật, rò rỉ dữ liệu.
* **Suggestion/Improvement:** Các đề xuất thay đổi để sản phẩm tốt hơn (không phải lỗi).

---

> [!IMPORTANT]
> **Lưu ý cho Workflow:**
> 1. **QA** thiết lập Severity. **PM/PO** có quyền quyết định cuối cùng về Priority.
> 2. **Severity** thường cố định xuyên suốt vòng đời bug, nhưng **Priority** có thể thay đổi tùy theo áp lực thời gian (ví dụ: lỗi Low có thể nhảy lên High khi gần ngày bàn giao).