# 🖱️ Hướng dẫn Google Ads Mouse Clicker

## 📋 **Tổng quan:**
Tool Google Ads Mouse Clicker sử dụng chuột thật và bàn phím thật để:
- ✅ **Click chuột thật** theo tọa độ đã cấu hình
- ✅ **Chuyển tab bằng bàn phím** (Ctrl+Tab)
- ✅ **Tự động tải file** mỗi 5 phút
- ✅ **Sử dụng Chrome đã mở sẵn**

## 🚀 **Cách sử dụng:**

### **Bước 1: Cài đặt dependencies**
```bash
pip install -r requirements_mouse_clicker.txt
```

### **Bước 2: Mở Chrome và các tab MCC**
- Mở Chrome bình thường
- Mở các tab Google Ads MCC đã đăng nhập
- Đảm bảo các tab đã load hoàn tất

### **Bước 3: Chạy tool**
```bash
python google_ads_mouse_clicker.py
```

### **Bước 4: Hiệu chỉnh tọa độ click**
- Chọn tùy chọn `5. Xem cấu hình` để xem tọa độ hiện tại
- Chỉnh sửa file `mouse_clicker_config.json` với tọa độ thực tế
- Chọn tùy chọn `4. Test click chuột` để kiểm tra

### **Bước 5: Bắt đầu chạy ngầm**
- Chọn tùy chọn `1. Bắt đầu chạy ngầm`
- Tool sẽ tự động click và tải file mỗi 5 phút

## 📁 **Files quan trọng:**

1. **`google_ads_mouse_clicker.py`** - Script chính
2. **`create_mouse_clicker_config.py`** - Tạo file cấu hình
3. **`mouse_clicker_config.json`** - File cấu hình
4. **`requirements_mouse_clicker.txt`** - Dependencies
5. **`HUONG_DAN_MOUSE_CLICKER.md`** - Hướng dẫn này

## ⚙️ **Cấu hình tọa độ click:**

### **File cấu hình: `mouse_clicker_config.json`**
```json
{
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
        }
    }
}
```

### **Cách lấy tọa độ:**
1. **Mở Chrome và các tab MCC**
2. **Chạy tool:** `python google_ads_mouse_clicker.py`
3. **Chọn tùy chọn 4:** Test click chuột
4. **Xem tọa độ hiện tại** và chỉnh sửa trong config
5. **Test lại** cho đến khi đúng

## 🔍 **Cách hoạt động:**

### **1. Click chuột thật**
- Sử dụng PyAutoGUI để click chuột
- Di chuyển chuột theo đường cong Bezier (giống người thật)
- Click theo tọa độ đã cấu hình

### **2. Chuyển tab bằng bàn phím**
- Sử dụng Ctrl+Tab để chuyển tab
- Tự động chuyển qua tất cả tab

### **3. Chạy ngầm mỗi 5 phút**
- Lập lịch xuất file mỗi 5 phút
- Tự động click và tải file
- Lưu kết quả và log

## 📊 **Menu điều khiển:**

```
📋 MENU:
1. Bắt đầu chạy ngầm      ← Chọn cái này
2. Dừng chạy ngầm
3. Xem trạng thái
4. Test click chuột        ← Test trước khi chạy
5. Xem cấu hình
6. Lưu kết quả ra CSV
7. Thoát
```

## 🐛 **Xử lý lỗi:**

### **Lỗi: "Tọa độ click không đúng"**
- **Nguyên nhân:** Tọa độ trong config không khớp với vị trí thực tế
- **Khắc phục:** Chỉnh sửa tọa độ trong `mouse_clicker_config.json`

### **Lỗi: "Không thể chuyển tab"**
- **Nguyên nhân:** Không có tab nào hoặc tab bị lỗi
- **Khắc phục:** Kiểm tra Chrome có tab nào không

### **Lỗi: "Click thất bại"**
- **Nguyên nhân:** Tọa độ click không chính xác
- **Khắc phục:** Test lại tọa độ và chỉnh sửa config

## 📈 **Theo dõi kết quả:**

### **Log file: `google_ads_mouse_clicker.log`**
- Ghi lại mọi thao tác click
- Hiển thị lỗi chi tiết
- Theo dõi tiến trình

### **Screenshot: Thư mục `screenshots/`**
- Chụp ảnh trước và sau mỗi thao tác
- Giúp debug khi cần
- Lưu theo timestamp

### **Kết quả CSV: `export_results_*.csv`**
- Lưu kết quả xuất file
- Thống kê thành công/thất bại
- Timestamp chi tiết

## 🔥 **Tips và Tricks:**

- **Test trước khi chạy:** Chọn tùy chọn 4 để kiểm tra tọa độ
- **Theo dõi log:** Xem file log để biết tool đang làm gì
- **Chụp screenshot:** Bật tính năng chụp ảnh để debug
- **Lưu kết quả:** Xuất kết quả ra CSV để phân tích
- **Tùy chỉnh thời gian:** Thay đổi interval trong config

## ⚠️ **Lưu ý quan trọng:**

- ✅ **Chrome phải mở trước** khi chạy tool
- ✅ **Các tab phải đã đăng nhập** Google Ads MCC
- ✅ **Không di chuyển chuột** khi tool đang chạy
- ✅ **Cần hiệu chỉnh tọa độ** cho phù hợp
- ✅ **Có thể dừng bất cứ lúc nào** bằng Ctrl+C

## 🎯 **Quy trình hoàn chỉnh:**

1. **Cài đặt dependencies** → `pip install -r requirements_mouse_clicker.txt`
2. **Mở Chrome và các tab MCC** → Đăng nhập Google Ads
3. **Chạy tool** → `python google_ads_mouse_clicker.py`
4. **Hiệu chỉnh tọa độ** → Chỉnh sửa config và test
5. **Bắt đầu chạy ngầm** → Chọn tùy chọn 1
6. **Theo dõi log** → Xem file `google_ads_mouse_clicker.log`
7. **Dừng khi cần** → Ctrl+C hoặc chọn tùy chọn 2

## 📞 **Hỗ trợ:**

Nếu gặp vấn đề, hãy:
1. Kiểm tra log file: `google_ads_mouse_clicker.log`
2. Kiểm tra screenshot trong thư mục `screenshots/`
3. Test tọa độ click bằng tùy chọn 4
4. Kiểm tra Chrome có hoạt động bình thường không
5. Thử chạy lại từ đầu

---

**🎉 Chúc bạn sử dụng tool thành công!**

**🖱️ Tool sẽ sử dụng chuột thật để click và tải file mỗi 5 phút!**
