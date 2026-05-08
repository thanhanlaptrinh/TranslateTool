import customtkinter as ctk
from googletrans import Translator
from PIL import ImageGrab
import pytesseract
import ctypes
import time
import os

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# Cấu hình đường dẫn (Đảm bảo file này tồn tại trên máy bạn)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ScreenSelector(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Khung Quét")
        self.attributes("-alpha", 0.3)
        self.attributes("-topmost", True)
        self.geometry("300x200+500+300")
        self.bind("<B1-Motion>", self.move_window)
        
    def move_window(self, event):
        self.geometry(f"+{event.x_root-50}+{event.y_root-20}")

class TranslateApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TRANSLATE TOOLS")
        self.geometry("600x480")
        self.configure(fg_color="#DDE6F5")
        
        self.translator = Translator()
        self.selector = None
        self.lang_config = {
            "TIẾNG ANH": ["en", "eng"],
            "TIẾNG VIỆT": ["vi", "vie"],
            "TIẾNG NHẬT": ["ja", "jpn"],
            "TIẾNG TRUNG": ["zh-cn", "chi_sim"]
        }

        ctk.CTkLabel(self, text="TRANSLATE TOOLS", font=("Arial", 20, "bold"), text_color="black").pack(pady=10)

        self.text_area = ctk.CTkTextbox(self, width=550, height=250, corner_radius=20, border_width=2, border_color="black", fg_color="white", text_color="black", font=("Arial", 14))
        self.text_area.pack(pady=10)
        self.text_area.insert("1.0", "HƯỚNG DẪN:\n1. Chọn vùng cần dịch.\n2. Bấm 'DỊCH VÙNG NÀY'.")

        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(pady=20, fill="x", padx=20)

        self.src_lang_combo = ctk.CTkComboBox(self.bottom_frame, values=list(self.lang_config.keys()), corner_radius=20)
        self.src_lang_combo.set("TIẾNG ANH")
        self.src_lang_combo.grid(row=0, column=0, padx=5)

        ctk.CTkLabel(self.bottom_frame, text="→", font=("Arial", 20), text_color="black").grid(row=0, column=1)

        self.dest_lang_combo = ctk.CTkComboBox(self.bottom_frame, values=list(self.lang_config.keys()), corner_radius=20)
        self.dest_lang_combo.set("TIẾNG VIỆT")
        self.dest_lang_combo.grid(row=0, column=2, padx=5)

        self.btn_action = ctk.CTkButton(self.bottom_frame, text="CHỌN VÙNG", command=self.toggle_selector, corner_radius=20, fg_color="#FFCC00", text_color="black")
        self.btn_action.grid(row=0, column=3, padx=10)

    def toggle_selector(self):
        if self.selector is None or not self.selector.winfo_exists():
            self.selector = ScreenSelector(self)
            self.btn_action.configure(text="DỊCH VÙNG NÀY")
        else:
            self.capture_and_translate()

    def capture_and_translate(self):
        # Lấy thông số khung quét
        x = self.selector.winfo_x()
        y = self.selector.winfo_y()
        w = self.selector.winfo_width()
        h = self.selector.winfo_height()

        # Tạm ẩn khung quét để chụp chữ rõ hơn
        self.selector.attributes("-alpha", 0.0)
        self.update()
        time.sleep(0.2) 

        # Chụp màn hình
        screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        
        # Hiện lại khung quét
        self.selector.attributes("-alpha", 0.3)

        try:
            # Lấy mã ngôn ngữ tương ứng
            src_name = self.src_lang_combo.get()
            dest_name = self.dest_lang_combo.get()
            
            tess_lang = self.lang_config[src_name][1]
            google_src = self.lang_config[src_name][0]
            google_dest = self.lang_config[dest_name][0]

            # 3. OCR VỚI NGÔN NGỮ ĐÃ CHỌN
            extracted_text = pytesseract.image_to_string(screenshot, lang=tess_lang).strip()
            
            if not extracted_text:
                self.text_area.delete("1.0", "end")
                self.text_area.insert("1.0", "KHÔNG ĐỌC ĐƯỢC CHỮ!\nHãy thử kéo khung quét rộng hơn hoặc kiểm tra xem vùng đó có chữ không.")
                return

            # Dịch
            translation = self.translator.translate(extracted_text, src=google_src, dest=google_dest)

            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", f"GỐC: {extracted_text}\n\n--- DỊCH ---\n\n{translation.text}")
            
        except Exception as e:
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", f"LỖI: {str(e)}\n\n(Nếu dịch Tiếng Nhật/Trung, hãy đảm bảo bạn đã cài gói ngôn ngữ cho Tesseract)")

if __name__ == "__main__":
    app = TranslateApp()
    app.mainloop()