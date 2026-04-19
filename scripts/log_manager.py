import pandas as pd
import os
from datetime import datetime
from sheet_logger import GoogleSheetManager # Import Manager mới

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
    base_dir = f"assets/{project_name}"
    file_path = f"{base_dir}/bug_tracking_db.xlsx"
    os.makedirs(base_dir, exist_ok=True)
    
    if "Date" not in bug_data or not bug_data["Date"]:
        bug_data["Date"] = datetime.now().strftime("%Y-%m-%d")
        
    row_data = {col: bug_data.get(col, "") for col in BUG_COLUMNS}
    df_new = pd.DataFrame([row_data])

    # 1. Backup vào file Excel local
    if not os.path.exists(file_path):
        df_new.to_excel(file_path, index=False)
    else:
        df_existing = pd.read_excel(file_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_excel(file_path, index=False)
        
    # 2. Đẩy lên Google Sheets
    gs_data_list = [row_data[col] for col in BUG_COLUMNS]
    gs_manager.log_data(project_name, "Bugs", gs_data_list)
    
    return f"Đã ghi log Bug thành công vào Local và Google Sheet của dự án {project_name}."

def log_testcase_to_project(project_name: str, tc_data: dict):
    """ Hàm mới dành riêng cho việc ghi Test Case """
    base_dir = f"assets/{project_name}"
    file_path = f"{base_dir}/testcase_db.xlsx"
    os.makedirs(base_dir, exist_ok=True)
    
    if "Date" not in tc_data or not tc_data["Date"]:
        tc_data["Date"] = datetime.now().strftime("%Y-%m-%d")
        
    row_data = {col: tc_data.get(col, "") for col in TC_COLUMNS}
    df_new = pd.DataFrame([row_data])

    # 1. Backup vào file Excel local
    if not os.path.exists(file_path):
        df_new.to_excel(file_path, index=False)
    else:
        df_existing = pd.read_excel(file_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_excel(file_path, index=False)
        
    # 2. Đẩy lên Google Sheets
    gs_data_list = [row_data[col] for col in TC_COLUMNS]
    gs_manager.log_data(project_name, "TestCases", gs_data_list)
    
    return f"Đã ghi log Test Case thành công vào Local và Google Sheet của dự án {project_name}."