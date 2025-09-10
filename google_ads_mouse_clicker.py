#!/usr/bin/env python3
"""
Google Ads Mouse Clicker - Tự động click chuột thật và chuyển tab bằng bàn phím
Author: Assistant
Version: 1.0
"""

import time
import random
import logging
from datetime import datetime, timedelta
import os
import json
import pandas as pd
from typing import Dict, List, Tuple, Optional
import threading
import queue
import schedule
import pyautogui
import pyperclip
from PIL import Image
import cv2
import numpy as np

class GoogleAdsMouseClicker:
    def __init__(self, config_file="mouse_clicker_config.json"):
        self.config_file = config_file
        self.setup_logging()
        self.load_config()
        self.running = False
        # Ngăn chặn chồng chéo chu kỳ
        self.cycle_running = False
        self.current_tab_index = 0
        self.results = []
        
        # Thiết lập PyAutoGUI
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
    def setup_logging(self):
        """Thiết lập logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('google_ads_mouse_clicker.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self):
        """Load cấu hình từ file JSON"""
        default_config = {
            "tab_names": [
                "MCC Account 1",
                "MCC Account 2", 
                "MCC Account 3"
            ],
        "click_positions": {
            "refresh_button": {
                "x": 1488,
                "y": 107,
                "description": "Nút Refresh"
            },
            "download_button": {
                # "x": 1680,
                # "y": 728,
                "description": "Nút Download"
            },
            "combobox_option": {
                "x": 1550,
                "y": 550,
                "description": "Tùy chọn trong combobox"
            }
        },
            "templates": {
                "refresh_button": [],
                "download_button": [],
                "combobox_option": []
            },
            "timing": {
                "export_interval_minutes": 5,
                "export_interval_seconds": None,
                "click_delay": 1,
                "tab_switch_delay": 2,
                "export_process_wait": 15,
                "page_load_wait": 3,
                "tabs_per_cycle": 1,
                "post_cycle_delay_seconds": 120
            },
            "mouse_settings": {
                "click_duration": 1,
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
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                self.logger.info(f"✅ Đã load config từ {self.config_file}")
            except Exception as e:
                self.logger.warning(f"⚠️ Lỗi load config: {e}, sử dụng config mặc định")
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()
            self.logger.info(f"✅ Đã tạo config mặc định: {self.config_file}")
            
    def save_config(self):
        """Lưu config ra file JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            self.logger.info(f"✅ Đã lưu config: {self.config_file}")
        except Exception as e:
            self.logger.error(f"❌ Lỗi lưu config: {e}")
            
    def human_like_delay(self, min_seconds=0.5, max_seconds=1.5):
        """Delay ngẫu nhiên giống người thật"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        
    def human_like_click(self, x, y, description=""):
        """Click chuột giống người thật"""
        try:
            self.logger.info(f"🖱️ Đang click {description} tại ({x}, {y})")
            
            # Lấy vị trí hiện tại của chuột
            current_x, current_y = pyautogui.position()
            
            # Tính toán đường đi ngẫu nhiên
            if self.config["mouse_settings"]["human_like"]:
                # Tạo đường cong Bezier ngẫu nhiên
                control_points = self.generate_bezier_points(
                    (current_x, current_y), (x, y)
                )
                
                # Di chuyển chuột theo đường cong
                for point in control_points:
                    pyautogui.moveTo(point[0], point[1], 
                                   duration=self.config["mouse_settings"]["move_duration"])
                    time.sleep(random.uniform(0.01, 0.05))
            
            # Click chuột
            pyautogui.click(x, y, duration=self.config["mouse_settings"]["click_duration"])
            
            # Delay sau khi click
            click_delay = self.config["timing"]["click_delay"]
            self.human_like_delay(click_delay * 0.5, click_delay * 1.5)
            
            self.logger.info(f"✅ Đã click {description}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Lỗi click {description}: {e}")
            return False
            
    def generate_bezier_points(self, start, end, num_points=10):
        """Tạo các điểm Bezier cho đường di chuyển chuột tự nhiên"""
        # Tạo control points ngẫu nhiên
        control1_x = start[0] + random.randint(-50, 50)
        control1_y = start[1] + random.randint(-50, 50)
        control2_x = end[0] + random.randint(-50, 50)
        control2_y = end[1] + random.randint(-50, 50)
        
        points = []
        for i in range(num_points + 1):
            t = i / num_points
            # Bezier curve formula
            x = (1-t)**3 * start[0] + 3*(1-t)**2*t * control1_x + 3*(1-t)*t**2 * control2_x + t**3 * end[0]
            y = (1-t)**3 * start[1] + 3*(1-t)**2*t * control1_y + 3*(1-t)*t**2 * control2_y + t**3 * end[1]
            points.append((int(x), int(y)))
            
        return points
        
    def switch_to_tab(self, tab_index):
        """Chuyển tab bằng Ctrl+Tab đơn giản - không click Chrome"""
        try:
            tab_name = self.config["tab_names"][tab_index] if tab_index < len(self.config["tab_names"]) else f"Tab {tab_index + 1}"
            self.logger.info(f"🔄 Đang chuyển sang {tab_name} (tab {tab_index + 1})")
            
            if tab_index == 0:
                self.logger.info("   Đã ở tab đầu tiên, không cần chuyển")
                return True
            
            # Chỉ bấm Ctrl+Tab, không click Chrome để tránh load lại trang
            for i in range(tab_index):
                self.logger.info(f"   Bấm Ctrl+Tab lần {i + 1}/{tab_index}")
                pyautogui.hotkey('ctrl', 'tab')
                time.sleep(1)  # Chỉ chờ 1 giây
            
            self.logger.info(f"✅ Đã chuyển sang {tab_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Lỗi chuyển tab: {e}")
            return False
            
    def take_screenshot(self, name="screenshot", tab_name=""):
        """Chụp screenshot và lưu"""
        try:
            if not self.config["export_settings"]["save_screenshots"]:
                return None
                
            screenshot_dir = self.config["export_settings"]["screenshot_dir"]
            os.makedirs(screenshot_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{screenshot_dir}/{tab_name}_{name}_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            
            self.logger.info(f"📸 Đã chụp screenshot: {filename}")
            return filename
            
        except Exception as e:
            self.logger.warning(f"⚠️ Lỗi chụp screenshot: {e}")
            return None

    def locate_and_click(self, template_keys: List[str], confidence: float = 0.85, description: str = "") -> bool:
        """Tìm nút bằng template images (UI cũ/mới) theo đa tỉ lệ và click. Trả về True nếu thành công."""
        try:
            templates_cfg = self.config.get("templates", {})
            paths: List[str] = []
            for key in template_keys:
                vals = templates_cfg.get(key, [])
                if isinstance(vals, list):
                    paths.extend(vals)
                elif isinstance(vals, str):
                    paths.append(vals)

            # Chuẩn bị ảnh màn hình xám một lần
            screen = pyautogui.screenshot()
            screen_np = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
            screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

            best = {"conf": 0.0, "center": None, "path": None}
            # Thử lần lượt từng template và nhiều tỉ lệ
            for path in paths:
                if not os.path.exists(path):
                    continue
                tpl = cv2.imread(path, cv2.IMREAD_COLOR)
                if tpl is None:
                    continue
                tpl_gray = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)

                # Multi-scale around 75%..130%
                for scale in np.linspace(0.75, 1.30, 12):
                    h0, w0 = tpl_gray.shape[:2]
                    h = int(h0 * scale)
                    w = int(w0 * scale)
                    if h < 10 or w < 10:
                        continue
                    if h >= screen_gray.shape[0] or w >= screen_gray.shape[1]:
                        continue
                    tpl_resized = cv2.resize(tpl_gray, (w, h), interpolation=cv2.INTER_AREA)
                    res = cv2.matchTemplate(screen_gray, tpl_resized, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                    if max_val > best["conf"]:
                        best["conf"] = max_val
                        best["center"] = (max_loc[0] + w // 2, max_loc[1] + h // 2)
                        best["path"] = path

            self.logger.info(f"🔎 {description or template_keys}: max confidence = {best['conf']:.3f} (template: {best['path']})")
            if best["conf"] >= confidence and best["center"] is not None:
                cx, cy = best["center"]
                self.logger.info(f"✅ Tìm thấy {description or template_keys} tại ({cx},{cy})")
                return self.human_like_click(cx, cy, description or ",".join(template_keys))

            self.logger.info(f"❌ Không tìm thấy {description or template_keys} bằng template với ngưỡng {confidence}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Lỗi locate_and_click: {e}")
            return False
            
    def export_for_tab(self, tab_index, retry_count=0):
        """Xuất file cho một tab cụ thể theo flow: Refresh → Download → Chọn combobox"""
        try:
            tab_name = self.config["tab_names"][tab_index] if tab_index < len(self.config["tab_names"]) else f"Tab {tab_index + 1}"
            self.logger.info(f"🚀 Bắt đầu xuất file cho {tab_name}")
            
            # Chờ trang ổn định trước khi bắt đầu
            self.logger.info("⏳ Chờ trang ổn định...")
            time.sleep(3)
            
            # Chụp screenshot trước khi bắt đầu
            self.take_screenshot("before_export", tab_name)

            # Bước 1: Refresh (CHỈ dùng template)
            self.logger.info("🔄 Refresh (image only)...")
            clicked_refresh = self.locate_and_click(["refresh_button"], confidence=0.8, description="Refresh (template)")
            if not clicked_refresh:
                self.logger.error("❌ Không tìm thấy nút Refresh bằng hình ảnh")
                return False
            self.take_screenshot("after_refresh_click", tab_name)
            page_load_wait = self.config["timing"].get("page_load_wait", 1)
            if page_load_wait > 0:
                self.logger.info(f"⏳ Chờ {page_load_wait} giây sau Refresh...")
                time.sleep(page_load_wait)
            
            # Bước 2: Click nút Download (CHỈ dùng template)
            self.logger.info("⬇️ Download (image only)...")
            # Hạ ngưỡng nhận diện dành riêng cho Download để tăng độ bền khi giao diện thay đổi
            clicked_download = self.locate_and_click(["download_button"], confidence=0.70, description="Download (template)")
            if not clicked_download:
                self.logger.error(f"❌ Không tìm thấy nút Download bằng hình ảnh cho {tab_name}")
                return False
                
            # Chụp screenshot sau khi click Download
            self.take_screenshot("after_download_click", tab_name)
            
            # Chờ combobox hiển thị
            self.logger.info("⏳ Chờ combobox hiển thị...")
            time.sleep(2)
            
            # Bước 3: Chọn tùy chọn trong combobox (.csv) (CHỈ dùng template)
            self.logger.info("📄 Chọn .csv (image only)...")
            clicked_csv = self.locate_and_click(["combobox_option"], confidence=0.8, description="CSV option (template)")
            if not clicked_csv:
                self.logger.error(f"❌ Không tìm thấy mục .csv trong combobox bằng hình ảnh cho {tab_name}")
                return False
                
            # Chụp screenshot sau khi chọn combobox
            self.take_screenshot("after_combobox_selection", tab_name)

            # Theo yêu cầu: click thêm 1 lần nữa vào vị trí combobox sau khi đã chọn
            try:
                self.logger.info("🖱️ Click thêm 1 lần nữa vào .csv để xác nhận/đóng menu (image only)")
                time.sleep(0.5)
                self.locate_and_click(["combobox_option"], confidence=0.8, description="CSV option (extra)")
            except Exception as _e:
                self.logger.warning(f"⚠️ Không thể click thêm lần nữa vào combobox: {_e}")
            
            # Chờ quá trình download hoàn tất
            export_wait = self.config["timing"]["export_process_wait"]
            self.logger.info(f"⏳ Chờ {export_wait} giây để download hoàn tất cho {tab_name}...")
            time.sleep(export_wait)
            
            # Chụp screenshot cuối cùng
            self.take_screenshot("download_completed", tab_name)
            
            self.logger.info(f"✅ Hoàn thành download cho {tab_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Lỗi download cho {tab_name}: {e}")
            
            # Retry nếu chưa vượt quá số lần thử
            max_retries = self.config["export_settings"]["max_retries"]
            if retry_count < max_retries:
                retry_delay = self.config["export_settings"]["retry_delay"]
                self.logger.info(f"🔄 Thử lại lần {retry_count + 1}/{max_retries} cho {tab_name} sau {retry_delay} giây...")
                time.sleep(retry_delay)
                return self.export_for_tab(tab_index, retry_count + 1)
            else:
                self.logger.error(f"❌ Đã thử {max_retries} lần nhưng vẫn thất bại cho {tab_name}")
                return False
                
    def reset_to_first_tab(self):
        """Reset về tab đầu tiên"""
        try:
            self.logger.info("🔄 Reset về tab đầu tiên...")
            # Đảm bảo Chrome được focus trước khi reset
            pyautogui.click(100, 100)
            time.sleep(1)
            
            # Sử dụng Ctrl + 1 để về tab đầu tiên
            pyautogui.hotkey('ctrl', '1')
            time.sleep(3)  # Tăng delay để tránh refresh
            
            # Chờ trang ổn định
            self.logger.info("⏳ Chờ trang ổn định sau khi reset...")
            time.sleep(5)
            
            self.logger.info("✅ Đã reset về tab đầu tiên")
            return True
        except Exception as e:
            self.logger.error(f"❌ Lỗi reset về tab đầu tiên: {e}")
            return False

    def debug_tab_info(self):
        """Debug thông tin tab"""
        try:
            self.logger.info("🔍 Debug thông tin tab:")
            self.logger.info(f"   Số tab trong config: {len(self.config['tab_names'])}")
            for i, name in enumerate(self.config["tab_names"]):
                self.logger.info(f"   Tab {i}: {name}")
        except Exception as e:
            self.logger.error(f"❌ Lỗi debug tab info: {e}")

    def run_export_cycle(self):
        """Chạy một chu kỳ download cho tất cả tab theo flow: Download → Combobox → Ctrl+Tab một lần giữa các tab (bỏ Refresh)"""
        try:
            # Chặn re-entry nếu chu kỳ trước chưa xong
            if self.cycle_running:
                self.logger.warning("⚠️ Chu kỳ trước chưa kết thúc, bỏ qua lần chạy này để tránh trùng lặp")
                return False
            self.cycle_running = True

            self.logger.info("🔄 Bắt đầu chu kỳ download")
            
            # Debug thông tin tab
            self.debug_tab_info()
            
            # Chờ một chút để đảm bảo Chrome sẵn sàng
            self.logger.info("⏳ Chờ Chrome sẵn sàng...")
            time.sleep(3)
            
            total_tabs_config = len(self.config["tab_names"])
            tabs_per_cycle_cfg = self.config["timing"].get("tabs_per_cycle")
            ctrl_tabs_per_cycle = self.config["timing"].get("ctrl_tabs_per_cycle")

            # Nếu cấu hình số lần bấm Ctrl+Tab, số tab xử lý = số lần bấm + 1
            if ctrl_tabs_per_cycle is not None:
                presses = int(max(0, ctrl_tabs_per_cycle))
                tabs_to_process = min(total_tabs_config, presses + 1)
                self.logger.info(f"📊 Sẽ bấm Ctrl+Tab {presses} lần → xử lý {tabs_to_process} tab")
            else:
                tabs_to_process = tabs_per_cycle_cfg or total_tabs_config
                tabs_to_process = max(1, min(tabs_to_process, total_tabs_config))
                presses = max(0, tabs_to_process - 1)
                self.logger.info(f"📊 Sẽ xử lý {tabs_to_process}/{total_tabs_config} tab trong chu kỳ này")

            # Xử lý tab đầu tiên (không bấm Ctrl+Tab)
            for i in range(tabs_to_process):
                tab_name = self.config["tab_names"][i]
                self.logger.info(f"📂 Xử lý tab {i+1}/{tabs_to_process}: {tab_name}")

                # Với các tab thứ 2 trở đi: bấm Ctrl+Tab đúng 1 lần cho mỗi tab
                if i > 0:
                    self.logger.info("   Ctrl+Tab sang tab kế tiếp")
                    pyautogui.hotkey('ctrl', 'tab')
                    time.sleep(self.config["timing"]["tab_switch_delay"])

                # Chờ trang load ngắn
                page_load_wait = self.config["timing"]["page_load_wait"]
                if page_load_wait > 0:
                    self.logger.info(f"⏳ Chờ {page_load_wait} giây để trang ổn định...")
                    time.sleep(page_load_wait)

                # Thực hiện flow cho tab hiện tại
                self.logger.info(f"🚀 Bắt đầu thực hiện flow cho {tab_name}")
                success = self.export_for_tab(i)
                
                # Lưu kết quả
                result = {
                    "tab_name": tab_name,
                    "tab_index": i,
                    "success": success,
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "error": None if success else "Download failed"
                }
                self.results.append(result)
                
                # Delay giữa các tab
                if i < tabs_to_process - 1:
                    self.logger.info("⏳ Delay ngắn giữa các tab...")
                    self.human_like_delay(0.8, 1.2)
                    
            # Sau khi hoàn tất tab cuối cùng, Ctrl+Tab thêm 1 lần theo yêu cầu
            try:
                if tabs_to_process > 0:
                    self.logger.info("➡️ Đã ở tab cuối cùng trong chu kỳ, Ctrl+Tab thêm 1 lần nữa")
                    pyautogui.hotkey('ctrl', 'tab')
                    time.sleep(self.config["timing"]["tab_switch_delay"])
            except Exception as _e:
                self.logger.warning(f"⚠️ Không thể Ctrl+Tab sau tab cuối: {_e}")

            # Không đảo về tab đầu tiên để tránh reset trang
            self.logger.info("✅ Hoàn thành chu kỳ download")
            # Chờ thêm theo cấu hình sau chu kỳ (ví dụ 120s)
            try:
                post_delay = int(self.config["timing"].get("post_cycle_delay_seconds", 0))
                if post_delay > 0:
                    self.logger.info(f"⏳ Chờ thêm {post_delay} giây trước khi chu kỳ tiếp theo...")
                    time.sleep(post_delay)
            except Exception as _e:
                self.logger.warning(f"⚠️ Không thể chờ sau chu kỳ: {_e}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Lỗi trong chu kỳ download: {e}")
            import traceback
            self.logger.error(f"Chi tiết lỗi: {traceback.format_exc()}")
            return False
        finally:
            self.cycle_running = False
            
    def start_background_export(self):
        """Bắt đầu chạy ngầm xuất file"""
        try:
            self.logger.info("🚀 Bắt đầu chạy ngầm xuất file")
            self.running = True
            
            # Lập lịch xuất file
            interval_seconds = self.config["timing"].get("export_interval_seconds")
            interval_minutes = self.config["timing"].get("export_interval_minutes", 5)
            if interval_seconds is not None:
                schedule.every(interval_seconds).seconds.do(self.run_export_cycle)
                self.logger.info(f"⏰ Đã lập lịch xuất file mỗi {interval_seconds} giây")
            else:
                schedule.every(interval_minutes).minutes.do(self.run_export_cycle)
                self.logger.info(f"⏰ Đã lập lịch xuất file mỗi {interval_minutes} phút")
            
            # Chạy ngay lần đầu
            self.run_export_cycle()
            
            # Vòng lặp chính
            while self.running:
                schedule.run_pending()
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            self.logger.info("⚠️ Đã dừng bởi người dùng")
            self.running = False
        except Exception as e:
            self.logger.error(f"❌ Lỗi trong chạy ngầm: {e}")
            self.running = False
                
    def stop_background_export(self):
        """Dừng chạy ngầm"""
        self.running = False
        self.logger.info("⏹️ Đã dừng chạy ngầm")
        
    def get_export_status(self):
        """Lấy trạng thái xuất file"""
        return {
            "running": self.running,
            "current_tab_index": self.current_tab_index,
            "total_tabs": len(self.config["tab_names"]),
            "total_exports": len(self.results),
            "successful_exports": len([r for r in self.results if r["success"]]),
            "failed_exports": len([r for r in self.results if not r["success"]])
        }
        
    def save_results_to_csv(self):
        """Lưu kết quả ra file CSV"""
        try:
            if not self.results:
                self.logger.warning("⚠️ Không có kết quả để lưu")
                return False
                
            df = pd.DataFrame(self.results)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_results_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8')
            
            self.logger.info(f"✅ Đã lưu kết quả: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Lỗi lưu kết quả: {e}")
            return False

def main():
    """Hàm main"""
    print("=== Google Ads Mouse Clicker ===")
    print("🖱️ Tool tự động click chuột thật theo flow: Refresh → Download → Combobox")
    print("🌐 Sử dụng Chrome đã mở sẵn")
    # Hiển thị lịch chạy theo giây nếu có
    try:
        _tmp_cfg = GoogleAdsMouseClicker().config
        _sec = _tmp_cfg["timing"].get("export_interval_seconds")
        if _sec is not None:
            print(f"⏰ Tự động thực hiện mỗi {_sec} giây")
        else:
            print(f"⏰ Tự động thực hiện mỗi {_tmp_cfg['timing'].get('export_interval_minutes', 5)} phút")
    except Exception:
        print("⏰ Tự động thực hiện theo cấu hình")
    print()
    print("📋 FLOW THỰC HIỆN:")
    print("1. Click nút Refresh")
    print("2. Click nút Download")
    print("3. Chọn tùy chọn trong combobox")
    print("4. Chuyển sang tab tiếp theo")
    print("5. Sau khi xử lý tất cả tab, chuyển về tab đầu tiên")
    print()
    print("📋 HƯỚNG DẪN:")
    print("1. Mở Chrome và các tab Google Ads MCC đã đăng nhập")
    print("2. Chạy tool này")
    print("3. Tool sẽ tự động thực hiện theo thời gian trong config")
    print()
    
    # Tạo instance
    clicker = GoogleAdsMouseClicker()
    
    while True:
        print("\n📋 MENU:")
        print("1. Bắt đầu chạy ngầm")
        print("2. Dừng chạy ngầm")
        print("3. Xem trạng thái")
        print("4. Test click chuột")
        print("5. Xem cấu hình")
        print("6. Lưu kết quả ra CSV")
        print("7. Thoát")
        
        choice = input("\nChọn tùy chọn (1-7): ").strip()
        
        if choice == '1':
            print("\n🚀 Bắt đầu chạy ngầm...")
            print("⚠️ Đảm bảo đã mở Chrome và các tab Google Ads MCC")
            confirm = input("Bạn có chắc chắn muốn tiếp tục? (y/N): ").strip().lower()
            if confirm == 'y':
                clicker.start_background_export()
            else:
                print("❌ Đã hủy")
                
        elif choice == '2':
            clicker.stop_background_export()
            
        elif choice == '3':
            status = clicker.get_export_status()
            print(f"\n📊 Trạng thái:")
            print(f"   Đang chạy: {'Có' if status['running'] else 'Không'}")
            print(f"   Tổng tab: {status['total_tabs']}")
            print(f"   Tổng lần xuất: {status['total_exports']}")
            print(f"   Thành công: {status['successful_exports']}")
            print(f"   Thất bại: {status['failed_exports']}")
            
        elif choice == '4':
            print("\n🖱️ Test click chuột...")
            print("⚠️ Đảm bảo đã mở Chrome và các tab Google Ads MCC")
            confirm = input("Bạn có chắc chắn muốn tiếp tục? (y/N): ").strip().lower()
            if confirm == 'y':
                print("\n🖱️ Test click chuột theo flow: Refresh → Download → Combobox...")
                for name, pos in clicker.config["click_positions"].items():
                    print(f"Click {name} tại ({pos['x']}, {pos['y']})")
                    if clicker.human_like_click(pos["x"], pos["y"], name):
                        print(f"✅ Click thành công: {name}")
                    else:
                        print(f"❌ Click thất bại: {name}")
                    time.sleep(2)
            
        elif choice == '5':
            print("\n📋 Cấu hình hiện tại:")
            print(f"   Số tab: {len(clicker.config['tab_names'])}")
            sec = clicker.config['timing'].get('export_interval_seconds')
            if sec is not None:
                print(f"   Interval: {sec} giây")
            else:
                print(f"   Interval: {clicker.config['timing'].get('export_interval_minutes', 5)} phút")
            print(f"   Click positions:")
            for name, pos in clicker.config["click_positions"].items():
                print(f"     {name}: ({pos['x']}, {pos['y']})")
        
        elif choice == '6':
            clicker.save_results_to_csv()
        
        elif choice == '7':
            print("👋 Tạm biệt!")
            break
        
        else:
            print("❌ Lựa chọn không hợp lệ")

if __name__ == "__main__":
    main()
