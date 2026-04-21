import os
import json
from datetime import datetime
from sheet_logger import GoogleSheetManager 

# [MỚI] Tự động trỏ ra thư mục gốc của toàn bộ dự án
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BUG_COLUMNS = [
    "Environment","Platform","Fixed Build Version", "Module", "Defect Name(sumary)", "Description", 
    "Expect", "Actual Result", "Type", "Severity", "Priority", "Status", 
    "Attachments", "Reported By", "DEV", "Date","Root Cause", "Note"
]

TC_COLUMNS = [
    "Test Case ID", "Title", "Module", "Type", "Priority", 
    "Pre-condition", "Steps", "Expected", "Actual", "Status", "Date", "Note"
]

# Khởi tạo GSheet Manager
gs_manager = GoogleSheetManager()

def log_bug_to_project(project_name: str, bug_data: dict):
    # Dùng đường dẫn tuyệt đối từ BASE_DIR
    project_dir = os.path.join(BASE_DIR, "assets", project_name)
    file_path = os.path.join(project_dir, "outputs", "bug_tracking_db.json")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    if "Date" not in bug_data or not bug_data["Date"]:
        bug_data["Date"] = datetime.now().strftime("%Y-%m-%d")
        
    # ====================================================
    # XỬ LÝ ATTACHMENT (UPLOAD LÊN DRIVE)
    # ====================================================
    attachment_name = str(bug_data.get("Attachments", "")).strip()
    
    if attachment_name and not attachment_name.startswith("http"):
        inputs_dir = os.path.join(project_dir, "inputs")
        input_file_path = os.path.join(inputs_dir, attachment_name)
        
        if os.path.exists(input_file_path):
            print(f"[Log Manager] Đang upload evidence '{attachment_name}' lên thư mục Drive...")
            drive_link = gs_manager.upload_evidence(project_name, input_file_path)            
            if drive_link:
                bug_data["Attachments"] = drive_link 
                print(f"[Log Manager] Upload thành công, link: {drive_link}")
            else:
                bug_data["Attachments"] = f"{attachment_name} (Lỗi upload Drive)"
        else:
            print(f"[Log Manager] Cảnh báo: Không tìm thấy file '{attachment_name}' trong thư mục {inputs_dir}.")
    # ====================================================

    row_data = {col: bug_data.get(col, "") for col in BUG_COLUMNS}

    # 1. Backup vào file JSON local
    existing_data = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
                
    existing_data.append(row_data)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
        
    # 2. Đẩy lên Google Sheets
    gs_data_list = [row_data[col] for col in BUG_COLUMNS]
    gs_manager.log_data(project_name, "Bugs", gs_data_list)
    
    return f"Đã ghi log Bug thành công vào Local (JSON trong outputs) và Google Sheet của dự án {project_name}."

def log_testcase_to_project(project_name: str, tc_data: dict):
    # Dùng đường dẫn tuyệt đối từ BASE_DIR
    project_dir = os.path.join(BASE_DIR, "assets", project_name)
    file_path = os.path.join(project_dir, "outputs", "testcase_db.json")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    if "Date" not in tc_data or not tc_data["Date"]:
        tc_data["Date"] = datetime.now().strftime("%Y-%m-%d")
        
    row_data = {col: tc_data.get(col, "") for col in TC_COLUMNS}

    # 1. Backup vào file JSON local
    existing_data = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
                
    existing_data.append(row_data)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
        
    # 2. Đẩy lên Google Sheets
    gs_data_list = [row_data[col] for col in TC_COLUMNS]
    gs_manager.log_data(project_name, "TestCases", gs_data_list)
    
    return f"Đã ghi log Test Case thành công vào Local (JSON trong outputs) và Google Sheet của dự án {project_name}."