import tkinter as tk
from tkinter import ttk, messagebox
import database as db


try:
    import ui_tivi, ui_khachhang, ui_nhacungcap, ui_nhanvien, ui_hoadon, ui_login 
except ImportError as e:
    messagebox.showerror("Lỗi thiếu file", f"Vui lòng kiểm tra file: {e}")

class MainMenu(tk.Frame):
    def __init__(self, parent, role, username='admin'):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.parent = parent
        self.role = role
        self.username = username
        self.windows = {} 

       
        self.color_bg = "#121212"      
        self.color_panel = "#1F1F1F"   
        self.color_accent = "#00E5FF"  
        self.color_text = "#FFFFFF"   
        self.color_btn = "#333333"     
        self.color_btn_hover = "#444444"

       
        empty_menu = tk.Menu(parent)
        parent.config(menu=empty_menu)

     
        self.setup_ui()

    def setup_ui(self):
      
        toolbar = tk.Frame(self, bg=self.color_panel, height=60)
        toolbar.pack(side=tk.TOP, fill=tk.X)

     
        lbl_brand = tk.Label(toolbar, text="📺 TV STORE PRO", 
                             bg=self.color_panel, fg=self.color_accent, 
                             font=("Segoe UI", 16, "bold"))
        lbl_brand.pack(side=tk.LEFT, padx=20)

     
        def create_btn(text, command, bg_color=self.color_panel):
            btn = tk.Button(toolbar, text=text, command=command,
                            bg=bg_color, fg="white", bd=0,
                            font=("Segoe UI", 11, "bold"),
                            padx=15, pady=10, cursor="hand2", activebackground="#00E5FF", activeforeground="black")
            btn.pack(side=tk.LEFT, padx=2)
            return btn

     
        create_btn("TRANG CHỦ", lambda: messagebox.showinfo("Info", "Bạn đang ở trang chủ"))

      
        if self.role == 'admin':
            create_btn("QUẢN LÝ SẢN PHẨM", self.mo_quan_ly_tivi)
            create_btn("NHÂN VIÊN", self.mo_quan_ly_nhan_vien)
            create_btn("KHÁCH HÀNG", self.mo_quan_ly_khach_hang)
            create_btn("NHÀ CUNG CẤP", self.mo_quan_ly_nha_cung_cap)
            create_btn("LỊCH SỬ HÓA ĐƠN", self.mo_quan_ly_hoa_don)

      
        if self.role == 'customer':
            create_btn("🛒 MUA SẮM TI VI", self.mo_quan_ly_tivi, bg_color="#2E7D32")
            create_btn("📦 GIỎ HÀNG CỦA TÔI", self.mo_quan_ly_hoa_don, bg_color="#E65100") 

      
        btn_exit = tk.Button(toolbar, text="ĐĂNG XUẤT", command=self.thoat,
                             bg="#D32F2F", fg="white", bd=0, font=("Segoe UI", 10, "bold"), padx=15)
        btn_exit.pack(side=tk.RIGHT, padx=10, pady=10)
        
    
        role_vn = "Quản Trị Viên" if self.role == 'admin' else "Khách Hàng"
        tk.Label(toolbar, text=f"{role_vn}: {self.username}", 
                 bg=self.color_panel, fg="#AAAAAA", font=("Arial", 10)).pack(side=tk.RIGHT, padx=10)


       
        self.main_canvas = tk.Canvas(self, bg=self.color_bg, highlightthickness=0)
        self.main_canvas.pack(fill=tk.BOTH, expand=True)

        self.draw_tv_background()
      
        self.bind("<Configure>", self.on_resize)

    def draw_tv_background(self):
        self.main_canvas.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        
        if w < 100: return

        center_x = w / 2
        center_y = h / 2

      
        tv_w, tv_h = 600, 350
        x1 = center_x - tv_w/2
        y1 = center_y - tv_h/2
        x2 = center_x + tv_w/2
        y2 = center_y + tv_h/2
        
      
        self.main_canvas.create_rectangle(x1-10, y1-10, x2+10, y2+20, fill="#333333", outline="#555555", width=2)
        
        self.main_canvas.create_rectangle(x1, y1, x2, y2, fill="#000000", outline="#222222")

    
        self.main_canvas.create_text(center_x, center_y - 20, text="CỬA HÀNG TI VI", 
                                     font=("Arial", 40, "bold"), fill=self.color_accent)
        
        self.main_canvas.create_text(center_x, center_y + 40, text="Công nghệ đỉnh cao - Hình ảnh sắc nét", 
                                     font=("Arial", 16), fill="#AAAAAA")
        
        self.main_canvas.create_text(center_x, center_y + 70, text="DPM215465 - Lê Quốc Hùng - DH23PM", 
                                     font=("Arial", 16), fill="#AAAAAA")

        self.main_canvas.create_oval(x2-30, y2+5, x2-20, y2+15, fill="red", outline="")

       
        if self.role == 'customer':
            
             btn_w = 200
             btn_h = 50
             bx1, by1 = center_x - btn_w/2, center_y + 100
             bx2, by2 = center_x + btn_w/2, center_y + 100 + btn_h
             
             self.main_canvas.create_rectangle(bx1, by1, bx2, by2, fill=self.color_accent, outline="white", width=2, tags="btn_mua")
             self.main_canvas.create_text(center_x, center_y + 125, text="BẮT ĐẦU MUA SẮM", font=("Arial", 12, "bold"), fill="black", tags="btn_mua")
             
             
             self.main_canvas.tag_bind("btn_mua", "<Button-1>", lambda e: self.mo_quan_ly_tivi())
             self.main_canvas.tag_bind("btn_mua", "<Enter>", lambda e: self.main_canvas.config(cursor="hand2"))
             self.main_canvas.tag_bind("btn_mua", "<Leave>", lambda e: self.main_canvas.config(cursor=""))

    def on_resize(self, event):
        self.draw_tv_background()

   
    def mo_form_chung(self, ten_key, title, size, UI_Class, **kwargs):
        self.parent.withdraw()
        window = tk.Toplevel(self.parent)
        window.title(title)
       
        try: window.state('zoomed') 
        except: window.attributes('-fullscreen', True)
        
        app = UI_Class(window, **kwargs)

        def on_close():
            window.destroy()
            self.parent.deiconify()
            try: self.parent.state('zoomed')
            except: pass
            self.parent.focus_force()

        window.protocol("WM_DELETE_WINDOW", on_close)

   
    def mo_quan_ly_tivi(self):
        self.mo_form_chung('tivi', "Sản Phẩm", "950x650", ui_tivi.QuanLyTivi, role=self.role, callback_mua=self.mo_quan_ly_hoa_don)
    def mo_quan_ly_khach_hang(self):
        self.mo_form_chung('khachhang', "Khách Hàng", "950x650", ui_khachhang.QuanLyKhachHang)
    def mo_quan_ly_nhan_vien(self):
        self.mo_form_chung('nhanvien', "Nhân Viên", "900x600", ui_nhanvien.QuanLyNhanVien)
    def mo_quan_ly_nha_cung_cap(self):
        self.mo_form_chung('ncc', "Nhà Cung Cấp", "800x500", ui_nhacungcap.QuanLyNhaCungCap)
    def mo_quan_ly_hoa_don(self):
        tieu_de = "Quản Lý Hóa Đơn" if self.role == 'admin' else "Giỏ Hàng Của Tôi"
        self.mo_form_chung('hoadon', tieu_de, "1100x700", ui_hoadon.QuanLyHoaDon, role=self.role, username=self.username)

    def thoat(self):
        if messagebox.askyesno("Đăng xuất", "Bạn muốn đăng xuất khỏi hệ thống?"):
            self.parent.destroy()


if __name__ == "__main__":
    conn = db.create_connection()
    if not conn: pass
    else:
        conn.close()
        
        root = tk.Tk() 
        root.title("Hệ Thống Quản Lý Cửa Hàng Ti Vi")
        root.configure(bg="#121212")
        root.withdraw() 
        
        login_window = ui_login.LoginWindow(root)
        root.wait_window(login_window) 

        if login_window.login_success:
            user_role = getattr(login_window, 'user_role', 'customer')
            current_username = getattr(login_window, 'logged_user', 'Guest')
            
            root.title(f"TV STORE PRO - [{current_username}]")
            
            try: root.state('zoomed') 
            except: root.attributes('-fullscreen', True)
            
            app = MainMenu(root, role=user_role, username=current_username)
            root.deiconify()
            root.mainloop()
        else:
            root.destroy()