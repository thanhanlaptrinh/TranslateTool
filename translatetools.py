import customtkinter as ctk
from googletrans import Translator
from PIL import ImageGrab
import pytesseract
import ctypes
import time

# Tối ưu độ phân giải màn hình
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# Đường dẫn Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ScreenSelector(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Vùng quét")
        self.attributes("-alpha", 0.3)
        self.attributes("-topmost", True)
        self.geometry("250x150+500+300")
        self.bind("<B1-Motion>", self.move_window)
        
    def move_window(self, event):
        self.geometry(f"+{event.x_root-50}+{event.y_root-20}")

class TranslateApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Translate Mini")
        self.geometry("400x350")
        self.configure(fg_color="#DDE6F5")
        self.attributes("-topmost", True)
        
        self.translator = Translator()
        self.selector = None
        self.lang_config = {
            "ANH": ["en", "eng"],
            "VIỆT": ["vi", "vie"],
            "NHẬT": ["ja", "jpn"],
            "TRUNG": ["zh-cn", "chi_sim"]
        }

        self.ctrl_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.ctrl_frame.pack(pady=10, fill="x", padx=10)

        self.src_lang = ctk.CTkComboBox(self.ctrl_frame, values=list(self.lang_config.keys()), width=90, corner_radius=10)
        self.src_lang.set("ANH")
        self.src_lang.grid(row=0, column=0, padx=2)

        ctk.CTkLabel(self.ctrl_frame, text="→", text_color="black", font=("Arial", 16)).grid(row=0, column=1)

        self.dest_lang = ctk.CTkComboBox(self.ctrl_frame, values=list(self.lang_config.keys()), width=90, corner_radius=10)
        self.dest_lang.set("VIỆT")
        self.dest_lang.grid(row=0, column=2, padx=2)

        self.btn_action = ctk.CTkButton(self.ctrl_frame, text="CHỌN VÙNG", command=self.toggle_selector, 
                                        width=110, height=32, corner_radius=10, fg_color="#FFCC00", text_color="black", font=("Arial", 12, "bold"))
        self.btn_action.grid(row=0, column=3, padx=5)

        self.text_area = ctk.CTkTextbox(self, width=380, height=260, corner_radius=15, border_width=1, 
                                        fg_color="white", text_color="black", font=("Arial", 13), wrap="word")
        self.text_area.pack(pady=(0, 10), padx=10)
        self.text_area.insert("1.0", "KẾT QUẢ DỊCH SẼ HIỆN Ở ĐÂY...")

    def toggle_selector(self):
        if self.selector is None or not self.selector.winfo_exists():
            self.selector = ScreenSelector(self)
            self.btn_action.configure(text="DỊCH NGAY", fg_color="#4CAF50", text_color="white")
        else:
            self.capture_and_translate()

    def capture_and_translate(self):
        x, y = self.selector.winfo_x(), self.selector.winfo_y()
        w, h = self.selector.winfo_width(), self.selector.winfo_height()

        self.selector.attributes("-alpha", 0.0)
        self.update()
        time.sleep(0.15) 

        screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        
        # Tiền xử lý ảnh để quét chữ game tốt hơn
        screenshot = screenshot.convert('L') 
        screenshot = screenshot.point(lambda x: 0 if x < 150 else 255, '1') 
        
        self.selector.attributes("-alpha", 0.3)

        try:
            src_key = self.src_lang.get()
            dest_key = self.dest_lang.get()
            
            # OCR với chế độ PSM 6 cho khối văn bản đơn lẻ
            extracted_text = pytesseract.image_to_string(
                screenshot, 
                lang=self.lang_config[src_key][1], 
                config='--psm 6'
            ).strip()
            
            if not extracted_text:
                self.update_result("❌ Không tìm thấy chữ. Hãy thử kéo khung rộng hơn.")
                return

            translation = self.translator.translate(
                extracted_text, 
                src=self.lang_config[src_key][0], 
                dest=self.lang_config[dest_key][0]
            )

            self.update_result(translation.text)
            
        except Exception as e:
            self.update_result(f"⚠️ Lỗi: {str(e)}")

    def update_result(self, content):
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", content)

if __name__ == "__main__":
    app = TranslateApp()
    app.mainloop()