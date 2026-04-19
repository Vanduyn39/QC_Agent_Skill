import gspread
from google.oauth2.service_account import Credentials
import json
import os

# Cấu hình kết nối
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Tự động trỏ ra thư mục gốc để lấy credentials.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")

# THAY BẰNG EMAIL THẬT CỦA BẠN ĐỂ SERVICE ACCOUNT SHARE QUYỀN
ADMIN_EMAIL = "your-email@gmail.com" 

class GoogleSheetManager:
    def __init__(self):
        try:
            credentials = Credentials.from_service_account_file(
                CREDENTIALS_FILE, scopes=SCOPES
            )
            self.client = gspread.authorize(credentials)
        except Exception as e:
            print(f"Lỗi kết nối Google Sheets: {e}")
            self.client = None

    def get_or_create_sheet(self, project_name, sheet_name):
        if not self.client:
            return None
        
        # 1. Tìm hoặc tạo file Google Sheet cho dự án
        try:
            spreadsheet = self.client.open(project_name)
        except gspread.exceptions.SpreadsheetNotFound:
            # Nếu chưa có thì tạo mới và share cho admin
            spreadsheet = self.client.create(project_name)
            if ADMIN_EMAIL and ADMIN_EMAIL != "your-email@gmail.com":
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
                worksheet.append_row(data)
                return True
            return False
        except Exception as e:
            print(f"[Sheet Logger] Lỗi khi ghi data: {e}")
            return False