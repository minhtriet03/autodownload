#!/usr/bin/env python3
"""
Tool lấy tọa độ chuột trên màn hình
"""

import pyautogui
import time
import sys

def get_mouse_position():
    """Lấy tọa độ chuột hiện tại"""
    print("🖱️ Tool lấy tọa độ chuột")
    print("=" * 50)
    print("Hướng dẫn:")
    print("1. Di chuyển chuột đến vị trí cần lấy tọa độ")
    print("2. Nhấn Ctrl+C để lấy tọa độ")
    print("3. Nhấn Ctrl+C lần nữa để thoát")
    print("=" * 50)
    
    try:
        while True:
            x, y = pyautogui.position()
            print(f"\rTọa độ hiện tại: ({x}, {y})", end="", flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        x, y = pyautogui.position()
        print(f"\n\n✅ Tọa độ cuối cùng: ({x}, {y})")
        print("📋 Copy tọa độ này vào file config:")
        print(f'   "x": {x},')
        print(f'   "y": {y},')
        
        # Hỏi có muốn lấy tọa độ khác không
        try:
            choice = input("\nBạn có muốn lấy tọa độ khác không? (y/N): ").strip().lower()
            if choice == 'y':
                get_mouse_position()
        except KeyboardInterrupt:
            print("\n👋 Tạm biệt!")

if __name__ == "__main__":
    get_mouse_position()
