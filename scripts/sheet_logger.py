import gspread
from google.oauth2.service_account import Credentials
import json
import os

# Connection configuration
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Automatically point to the root directory to get credentials.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")

# REPLACE WITH YOUR REAL EMAIL SO THE SERVICE ACCOUNT CAN SHARE PERMISSIONS
ADMIN_EMAIL = "your-email@gmail.com" 

class GoogleSheetManager:
    def __init__(self):
        try:
            credentials = Credentials.from_service_account_file(
                CREDENTIALS_FILE, scopes=SCOPES
            )
            self.client = gspread.authorize(credentials)
        except Exception as e:
            print(f"Google Sheets connection error: {e}")
            self.client = None

    def get_or_create_sheet(self, project_name, sheet_name):
        if not self.client:
            return None
        
        # 1. Find or create a Google Sheet file for the project
        try:
            spreadsheet = self.client.open(project_name)
        except gspread.exceptions.SpreadsheetNotFound:
            # If it doesn't exist, create a new one and share it with the admin
            spreadsheet = self.client.create(project_name)
            if ADMIN_EMAIL and ADMIN_EMAIL != "your-email@gmail.com":
                spreadsheet.share(ADMIN_EMAIL, perm_type='user', role='writer')
            print(f"[Sheet Logger] Created a new Sheet file for project: {project_name}")

        # 2. Find or create a Tab (Worksheet) inside the file
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="20")
            
            # Automatically insert Header depending on Log type
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
            print(f"[Sheet Logger] Error writing data: {e}")
            return False
