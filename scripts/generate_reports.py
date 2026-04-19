import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

# ==========================================
# CẤU HÌNH GOOGLE SHEETS
# ==========================================
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "credentials.json"

def sync_data_from_sheets(project_name: str):
    """Kéo dữ liệu mới nhất từ tab 'Bugs' trên Google Sheets về lưu đè lên file Excel local"""
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)
        
        # Mở file Google Sheet theo tên dự án
        spreadsheet = client.open(project_name) 
        
        # LẤY CHÍNH XÁC TỪ TAB "Bugs"
        worksheet = spreadsheet.worksheet("Bugs") 
        
        # Lấy toàn bộ dữ liệu
        data = worksheet.get_all_records()
        if data:
            df_sheets = pd.DataFrame(data)
            file_path = f"assets/{project_name}/bug_tracking_db.xlsx"
            
            # Đảm bảo thư mục tồn tại trước khi lưu
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Lưu đè lại file Excel cục bộ
            df_sheets.to_excel(file_path, index=False)
            print(f"[Sync] Đã đồng bộ dữ liệu mới nhất từ tab 'Bugs' Google Sheets cho dự án {project_name}.")
            return True
    except Exception as e:
        print(f"[Sync Warning] Không thể đồng bộ từ Google Sheets, sẽ dùng dữ liệu local: {e}")
    return False

# ==========================================
# HÀM XUẤT BÁO CÁO CHÍNH
# ==========================================
def get_project_report(project_name: str, mode: str = "daily", start_date: str = None, end_date: str = None):
    # 1. ĐỒNG BỘ DATA TỪ CLOUD VỀ LOCAL TRƯỚC
    sync_data_from_sheets(project_name)

    # 2. XỬ LÝ LOGIC VẼ BIỂU ĐỒ
    file_path = f"assets/{project_name}/bug_tracking_db.xlsx"
    output_dir = f"assets/{project_name}/outputs"
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(file_path):
        return json.dumps({"error": f"Không tìm thấy file tracking lỗi cho {project_name}."})

    try:
        df = pd.read_excel(file_path)
        # Ép kiểu cột Date để so sánh
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='mixed', dayfirst=True)
        
        now = datetime.now()
        today = pd.to_datetime(now.strftime("%Y-%m-%d"))
        
        # XỬ LÝ LỌC THỜI GIAN THEO MODE
        if mode == "daily":
            df_filtered = df[df['Date'] == today]
            today_str = now.strftime("%Y-%m-%d")
            chart_title = f"DAILY BUG DASHBOARD - {project_name.upper()}\n({today_str})"
            chart_filename = f"daily_dashboard_{today_str}.png"
            
        elif mode == "weekly":
            monday = today - timedelta(days=today.weekday())
            friday = monday + timedelta(days=4)
            df_filtered = df[(df['Date'] >= monday) & (df['Date'] <= friday)]
            monday_str = monday.strftime("%Y-%m-%d")
            friday_str = friday.strftime("%Y-%m-%d")
            chart_title = f"WEEKLY BUG DASHBOARD - {project_name.upper()}\n({monday_str} to {friday_str})"
            chart_filename = f"weekly_dashboard_{monday_str}_to_{friday_str}.png"
            
        elif mode == "custom":
            if not start_date or not end_date:
                return json.dumps({"error": "Chế độ custom yêu cầu phải có start_date và end_date (YYYY-MM-DD)."})
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            df_filtered = df[(df['Date'] >= start_dt) & (df['Date'] <= end_dt)]
            chart_title = f"CUSTOM BUG DASHBOARD - {project_name.upper()}\n({start_date} to {end_date})"
            chart_filename = f"custom_dashboard_{start_date}_to_{end_date}.png"
            
        else:
            return json.dumps({"error": "Mode không hợp lệ (chỉ hỗ trợ daily/weekly/custom)."})

        if df_filtered.empty:
            return json.dumps({"message": f"Không có bug nào được log trong khoảng thời gian này."})

        # ==========================================
        # VẼ DASHBOARD NHIỀU BIỂU ĐỒ (SUBPLOTS)
        # ==========================================
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle(chart_title, fontsize=18, fontweight='bold', y=1.02)
        axes = axes.flatten() 
        
        charts_to_draw = [
            ("Module", "Defect by Module"),
            ("Severity", "Defect by Severity"),
            ("Priority", "Defect by Priority"),
            ("Type", "Defect by Type")
        ]
        
        if "Root Cause" in df.columns:
            charts_to_draw.append(("Root Cause", "Root Cause Analysis"))
        elif "Status" in df.columns:
            charts_to_draw.append(("Status", "Defect by Status")) 

        # 1. Hàm vẽ biểu đồ tròn (Pie Chart) cho các trường phân loại
        def draw_pie_chart(ax, data_series, title):
            if data_series.empty:
                ax.axis('off')
                return
            wedges, texts, autotexts = ax.pie(
                data_series, autopct='%1.1f%%', startangle=140, 
                colors=plt.cm.Set3.colors,
                textprops={'fontsize': 10, 'weight': 'bold'},
                wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
            )
            ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
            ax.legend(wedges, data_series.index, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)

        # 2. Hàm vẽ biểu đồ cột (Bar Chart) dành riêng cho Module
        def draw_bar_chart(ax, data_series, title):
            if data_series.empty:
                ax.axis('off')
                return
            
            # Tạo danh sách màu (dùng bộ màu Set3 cho đồng bộ với các Pie Chart)
            # Dùng toán tử % để tự động lặp lại màu nếu số lượng Module nhiều hơn số màu có sẵn
            bar_colors = [plt.cm.Set3.colors[i % len(plt.cm.Set3.colors)] for i in range(len(data_series))]
            
            # Vẽ cột với danh sách màu vừa tạo
            bars = ax.bar(data_series.index, data_series.values, color=bar_colors, edgecolor='black', alpha=0.9)
            ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
            ax.set_ylabel("Number of Bugs", fontweight='bold')
            
            # Xoay tên các module nghiêng 45 độ để không bị đè lên nhau
            ax.tick_params(axis='x', rotation=45)
            for tick in ax.get_xticklabels():
                tick.set_horizontalalignment('right')
                
            # Ghi số lượng bug ở đỉnh từng cột
            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom', fontweight='bold')
        # Lặp để vẽ từng biểu đồ dựa theo Logic
        for i, (col_name, chart_name) in enumerate(charts_to_draw):
            if col_name in df_filtered.columns:
                counts = df_filtered[col_name].value_counts()
                
                # NẾU LÀ MODULE THÌ GỌI HÀM VẼ CỘT, CÒN LẠI VẼ TRÒN
                if col_name == "Module":
                    draw_bar_chart(axes[i], counts, chart_name)
                else:
                    draw_pie_chart(axes[i], counts, chart_name)
            else:
                axes[i].axis('off')

        # Tắt (ẩn) các ô trống không dùng đến trong khung 2x3
        for j in range(len(charts_to_draw), len(axes)):
            axes[j].axis('off')

        plt.tight_layout()
        
        # Lưu file
        chart_path = f"{output_dir}/{chart_filename}"
        plt.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close()

        # Tổng hợp dữ liệu trả về cho AI (để nó phân tích bằng text)
        stats = {
            "total_bugs": len(df_filtered),
            "by_module": df_filtered['Module'].value_counts().to_dict() if 'Module' in df.columns else {},
            "by_severity": df_filtered['Severity'].value_counts().to_dict() if 'Severity' in df.columns else {},
            "by_priority": df_filtered['Priority'].value_counts().to_dict() if 'Priority' in df.columns else {},
            "chart_path": chart_path,
            "note": "Data up-to-date with Google Sheets."
        }
        return json.dumps(stats, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({"error": f"Lỗi xử lý file: {str(e)}"})