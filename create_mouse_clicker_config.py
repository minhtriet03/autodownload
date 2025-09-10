#!/usr/bin/env python3
"""
Script tạo file cấu hình cho Google Ads Mouse Clicker
"""

import json
import os

def create_mouse_clicker_config():
    """Tạo file cấu hình cho Google Ads Mouse Clicker"""
    
    config = {
        "tab_names": [
            "MCC Account 1",
            "MCC Account 2", 
            "MCC Account 3"
        ],
        "click_positions": {
            "reports_menu": {
                "x": 100,
                "y": 200,
                "description": "Menu Reports"
            },
            "export_button": {
                "x": 300,
                "y": 400,
                "description": "Nút Export"
            },
            "google_sheets_option": {
                "x": 500,
                "y": 600,
                "description": "Tùy chọn Google Sheets"
            },
            "export_confirm": {
                "x": 700,
                "y": 800,
                "description": "Xác nhận xuất file"
            },
            "download_button": {
                "x": 900,
                "y": 1000,
                "description": "Nút Download"
            }
        },
        "timing": {
            "export_interval_minutes": 5,
            "click_delay": 1,
            "tab_switch_delay": 2,
            "export_process_wait": 15,
            "page_load_wait": 3
        },
        "mouse_settings": {
            "click_duration": 0.1,
            "move_duration": 0.5,
            "human_like": True
        },
        "export_settings": {
            "max_retries": 3,
            "retry_delay": 5,
            "save_screenshots": True,
            "screenshot_dir": "screenshots"
        }
    }
    
    # Lưu file cấu hình
    config_file = "mouse_clicker_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Đã tạo file cấu hình: {config_file}")
    print("\n📋 Hướng dẫn sử dụng:")
    print("1. Mở Chrome và các tab Google Ads MCC đã đăng nhập")
    print("2. Chạy script google_ads_mouse_clicker.py")
    print("3. Chọn tùy chọn '4. Test click chuột' để kiểm tra")
    print("4. Chọn tùy chọn '1. Bắt đầu chạy ngầm' để bắt đầu")
    print("5. Tool sẽ tự động tải file mỗi 5 phút")
    print()
    print("🎯 Các thông tin cần cấu hình:")
    print("- tab_names: Tên các tab (có thể thay đổi)")
    print("- click_positions: Tọa độ click chuột (cần hiệu chỉnh)")
    print("- timing: Thời gian và delay (có thể tùy chỉnh)")
    print()
    print("🔍 Cách hoạt động:")
    print("- Tool sử dụng chuột thật để click")
    print("- Chuyển tab bằng bàn phím (Ctrl+Tab)")
    print("- Chạy ngầm mỗi 5 phút (có thể tùy chỉnh)")
    print("- Tự động click theo tọa độ đã cấu hình")
    print()
    print("⚠️ Lưu ý:")
    print("- Phải mở Chrome và các tab trước khi chạy tool")
    print("- Các tab phải đã đăng nhập Google Ads")
    print("- Cần hiệu chỉnh tọa độ click cho phù hợp")
    print("- Tool sẽ click chuột thật nên không được di chuyển chuột")

if __name__ == "__main__":
    create_mouse_clicker_config()
