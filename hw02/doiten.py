import os
import pytesseract
from PIL import Image
import re

# ==========================================================
# CẤU HÌNH ĐƯỜNG DẪN (BẮT BUỘC CHỈNH SỬA)
# ==========================================================

# 1. Đường dẫn đến file tesseract.exe (Kiểm tra kỹ trong ổ C của bạn)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ngocs\Downloads\tesseract-5.5.2\tesseract-5.5.2'

# 2. Đường dẫn đến thư mục chứa các tấm ảnh cần đổi tên
# Lưu ý: Dùng dấu gạch chéo / hoặc thêm chữ r phía trước như ví dụ dưới
FOLDER_PATH = r'C:\Users\ngocs\Pictures\AnhCanDoiTen'

# ==========================================================

def clean_filename(text):
    """Làm sạch chuỗi để không chứa ký tự đặc biệt gây lỗi đặt tên file"""
    # Chỉ giữ lại chữ cái, số, khoảng trắng và dấu gạch ngang
    clean_text = re.sub(r'[\\/*?:"<>|]', '', text) 
    # Cắt bớt độ dài nếu quá dài (tối đa 50 ký tự) và xóa khoảng trắng thừa
    return clean_text.strip()[:50]

def batch_rename_images():
    # Kiểm tra thư mục có tồn tại không
    if not os.path.exists(FOLDER_PATH):
        print(f"Lỗi: Không tìm thấy thư mục tại {FOLDER_PATH}")
        return

    print("Đang bắt đầu xử lý...")
    
    count = 0
    for filename in os.listdir(FOLDER_PATH):
        # Kiểm tra định dạng file ảnh
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            old_path = os.path.join(FOLDER_PATH, filename)
            
            try:
                # Mở ảnh và nhận diện chữ (hỗ trợ Tiếng Việt + Tiếng Anh)
                image = Image.open(old_path)
                content = pytesseract.image_to_string(image, lang='vie+eng')
                
                # Làm sạch nội dung để đặt tên
                new_name_base = clean_filename(content)
                
                if not new_name_base:
                    print(f"Bỏ qua {filename}: Không tìm thấy chữ bên trong.")
                    continue
                
                # Tạo đường dẫn mới
                extension = os.path.splitext(filename)[1]
                new_filename = f"{new_name_base}{extension}"
                new_path = os.path.join(FOLDER_PATH, new_filename)
                
                # Tránh trùng tên file đã tồn tại
                suffix = 1
                while os.path.exists(new_path):
                    new_filename = f"{new_name_base}_{suffix}{extension}"
                    new_path = os.path.join(FOLDER_PATH, new_filename)
                    suffix += 1
                
                # Thực hiện đổi tên
                os.rename(old_path, new_path)
                print(f"Thành công: {filename} -> {new_filename}")
                count += 1
                
            except Exception as e:
                print(f"Lỗi khi xử lý file {filename}: {e}")

    print(f"\nHoàn tất! Đã đổi tên thành công {count} tệp tin.")

if __name__ == "__main__":
    batch_rename_images()