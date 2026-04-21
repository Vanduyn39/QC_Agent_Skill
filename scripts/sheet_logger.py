import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json
import os
import mimetypes

# Cấu hình kết nối
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Tự động trỏ ra thư mục gốc để lấy credentials.json và projects_config.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
PROJECTS_CONFIG_FILE = os.path.join(BASE_DIR, "projects_config.json") # <== [MỚI]

# THAY BẰNG EMAIL THẬT CỦA BẠN ĐỂ SERVICE ACCOUNT SHARE QUYỀN
ADMIN_EMAIL = "vanessa.phan.gos@gmail.com" 

class GoogleSheetManager:
    def __init__(self):
        try:
            credentials = Credentials.from_service_account_file(
                CREDENTIALS_FILE, scopes=SCOPES
            )
            self.client = gspread.authorize(credentials)
            
            # Khởi tạo thêm Drive API Service
            self.drive_service = build('drive', 'v3', credentials=credentials)
        except Exception as e:
            print(f"Lỗi kết nối Google Sheets/Drive: {e}")
            self.client = None
            self.drive_service = None

    # [MỚI] Hàm đọc cấu hình của dự án từ file JSON
    def get_project_config(self, project_name):
        if os.path.exists(PROJECTS_CONFIG_FILE):
            with open(PROJECTS_CONFIG_FILE, 'r', encoding='utf-8') as f:
                try:
                    configs = json.load(f)
                    return configs.get(project_name, {})
                except json.JSONDecodeError:
                    print("[Config Warning] File projects_config.json bị lỗi định dạng.")
        return {}

    def get_or_create_sheet(self, project_name, sheet_name):
        if not self.client:
            return None
        
        # 1. Tìm hoặc tạo file Google Sheet cho dự án
        try:
            spreadsheet = self.client.open(project_name)
        except gspread.exceptions.SpreadsheetNotFound:
            # Nếu chưa có thì tạo mới và share cho admin
            spreadsheet = self.client.create(project_name)
            if ADMIN_EMAIL and ADMIN_EMAIL != "vanessa.phan.gos@gmail.com":
                spreadsheet.share(ADMIN_EMAIL, perm_type='user', role='writer')
            print(f"[Sheet Logger] Đã tạo file Sheet mới cho dự án: {project_name}")

        # 2. Tìm hoặc tạo Tab (Worksheet) bên trong file
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="20")
            
            # Tự động chèn Header tùy theo loại Log
            if sheet_name == "Bugs":
                headers = ["Environment", "Platform", "Fixed Build Version", "Module", "Defect Name(sumary)", "Description", "Expect", "Actual Result", "Type", "Severity", "Priority", "Status", "Attachments", "Reported By", "DEV", "Date","Root Cause", "Note"]
                worksheet.append_row(headers)
            elif sheet_name == "TestCases": 
                headers = ["Test Case ID", "Title", "Module", "Type", "Priority", "Pre-condition", "Steps", "Expected", "Actual", "Status", "Date", "Note"]
                worksheet.append_row(headers)
                
        return worksheet

    def log_data(self, project_name, sheet_name, data: list):
        try:
            worksheet = self.get_or_create_sheet(project_name, sheet_name)
            if worksheet:
                # 1. Lấy toàn bộ dữ liệu thực tế (hàm này tự động bỏ qua các dòng trống dính format)
                all_values = worksheet.get_all_values()
                
                # 2. Tính toán chính xác số thứ tự của dòng tiếp theo
                next_row_index = len(all_values) + 1
                
                # 3. Ép Google chèn đúng vào vị trí đó (bỏ qua mọi lỗi nhảy dòng)
                worksheet.insert_row(data, index=next_row_index, value_input_option="USER_ENTERED")
                return True
            return False
        except Exception as e:
            print(f"[Sheet Logger] Lỗi khi ghi data: {e}")
            return False

    # ====================================================
    # [CẬP NHẬT] HÀM UPLOAD EVIDENCE LÊN GOOGLE DRIVE THEO DỰ ÁN
    # ====================================================
    def upload_evidence(self, project_name, file_path):
        if not self.drive_service:
            return ""
        try:
            # Đọc config để lấy thư mục Drive tương ứng với project_name
            config = self.get_project_config(project_name)
            EVIDENCE_FOLDER_ID = config.get("drive_folder_id")
            
            if not EVIDENCE_FOLDER_ID:
                print(f"[Drive Logger] Cảnh báo: Dự án '{project_name}' chưa được cấu hình 'drive_folder_id' trong projects_config.json")
                return ""

            file_name = os.path.basename(file_path)
            
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = 'application/octet-stream'

            file_metadata = {
                'name': file_name,
                'parents': [EVIDENCE_FOLDER_ID],
                'mimeType': mime_type
            }
            
            media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
            
            # Thực thi upload
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink',
                supportsAllDrives=True
            ).execute()
            
            file_id = file.get('id')
            
            # Phân quyền cho phép bất kỳ ai có link đều xem được
            permission = {'type': 'anyone', 'role': 'reader'}
            self.drive_service.permissions().create(
                fileId=file_id,
                body=permission,
                fields='id',
                supportsAllDrives=True
            ).execute()
            
            # Trả về link chia sẻ
            return file.get('webViewLink')
        except Exception as e:
            print(f"[Drive Logger] Lỗi upload file: {e}")
            return ""