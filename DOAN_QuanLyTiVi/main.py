import tkinter as tk
from tkinter import ttk, messagebox
import database as db


try:
    import ui_tivi, ui_khachhang, ui_nhacungcap, ui_nhanvien, ui_hoadon, ui_login, ui_baocao
except ImportError as e:

    print(f"Lưu ý: Chưa có file module con: {e}") 

class MainMenu(tk.Frame):
    def __init__(self, parent, role, username='admin'):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.parent = parent
        self.role = role
        self.username = username
        self.windows = {} 

        self.color_bg = "#121212"     
        self.color_panel = "#E0E0E0"   
        self.color_accent = "#0078D7"   
        

        self.font_menu = ("Segoe UI", 12)          
        self.font_brand = ("Segoe UI", 20, "bold") 


        empty_menu = tk.Menu(parent)
        parent.config(menu=empty_menu)

        self.create_toolbar()

        self.create_background()

    def create_toolbar(self):

        toolbar = tk.Frame(self, bg=self.color_panel, height=50)
        toolbar.pack(side=tk.TOP, fill=tk.X)


        lbl_brand = tk.Label(toolbar, text="📺 TV STORE", bg=self.color_panel, fg=self.color_accent, font=self.font_brand)
        lbl_brand.pack(side=tk.LEFT, padx=(15, 20), pady=5)

     
        mb_file = tk.Menubutton(toolbar, text="Tập tin", bg=self.color_panel, activebackground="#CCC", bd=0, font=self.font_menu)
        menu_file = tk.Menu(mb_file, tearoff=0, bg="white", activebackground=self.color_accent, activeforeground="white", font=self.font_menu)
        menu_file.add_command(label="Đăng xuất", command=self.thoat)
        menu_file.add_separator()
        menu_file.add_command(label="Thoát chương trình", command=self.parent.destroy)
        mb_file.config(menu=menu_file)
        mb_file.pack(side=tk.LEFT, padx=5)

        if self.role == 'admin':
            mb_cat = tk.Menubutton(toolbar, text="Danh mục", bg=self.color_panel, activebackground="#CCC", bd=0, font=self.font_menu)
            menu_cat = tk.Menu(mb_cat, tearoff=0, bg="white", activebackground=self.color_accent, activeforeground="white", font=self.font_menu)
            menu_cat.add_command(label="Sản phẩm (Ti Vi)", command=self.mo_quan_ly_tivi)
            menu_cat.add_command(label="Nhân viên", command=self.mo_quan_ly_nhan_vien)
            menu_cat.add_command(label="Khách hàng", command=self.mo_quan_ly_khach_hang)
            menu_cat.add_command(label="Nhà cung cấp", command=self.mo_quan_ly_nha_cung_cap)
            mb_cat.config(menu=menu_cat)
            mb_cat.pack(side=tk.LEFT, padx=5)

            mb_report = tk.Menubutton(toolbar, text="Báo cáo", bg=self.color_panel, activebackground="#CCC", bd=0, font=self.font_menu)
            menu_report = tk.Menu(mb_report, tearoff=0, bg="white", activebackground=self.color_accent, activeforeground="white", font=self.font_menu)
            menu_report.add_command(label="Hàng tồn kho", command=self.mo_bao_cao_hang_ton)
            menu_report.add_command(label="Doanh thu", command=self.mo_bao_cao_doanh_thu)
            mb_report.config(menu=menu_report)
            mb_report.pack(side=tk.LEFT, padx=5)


        mb_bill = tk.Menubutton(toolbar, text="Hóa đơn", bg=self.color_panel, activebackground="#CCC", bd=0, font=self.font_menu)
        menu_bill = tk.Menu(mb_bill, tearoff=0, bg="white", activebackground=self.color_accent, activeforeground="white", font=self.font_menu)
        lbl_hd = "Quản lý Hóa đơn" if self.role == 'admin' else "Giỏ hàng của tôi"
        menu_bill.add_command(label=lbl_hd, command=self.mo_quan_ly_hoa_don)
        mb_bill.config(menu=menu_bill)
        mb_bill.pack(side=tk.LEFT, padx=5)


        mb_help = tk.Menubutton(toolbar, text="Trợ giúp", bg=self.color_panel, activebackground="#CCC", bd=0, font=self.font_menu)
        menu_help = tk.Menu(mb_help, tearoff=0, bg="white", activebackground=self.color_accent, activeforeground="white", font=self.font_menu)
        menu_help.add_command(label="Thông tin tác giả", command=lambda: messagebox.showinfo("Info", "DPM215465 - Lê Quốc Hùng"))
        mb_help.config(menu=menu_help)
        mb_help.pack(side=tk.LEFT, padx=5)


        search_frame = tk.Frame(toolbar, bg=self.color_panel)
        search_frame.pack(side=tk.RIGHT, padx=20)

        self.ent_search = ttk.Entry(search_frame, width=30, font=self.font_menu)
        self.ent_search.pack(side=tk.LEFT, padx=5, ipady=3) 
        self.ent_search.bind("<Return>", lambda event: self.tim_kiem_nhanh())

        btn_search = tk.Button(search_frame, text="🔍 Tìm", command=self.tim_kiem_nhanh, 
                               bg=self.color_accent, fg="white", bd=0, padx=10, font=self.font_menu)
        btn_search.pack(side=tk.LEFT)


        role_vn = "Admin" if self.role == 'admin' else "Khách"
        tk.Label(toolbar, text=f"{role_vn}: {self.username} |", bg=self.color_panel, fg="#555", font=self.font_menu).pack(side=tk.RIGHT)

    def create_background(self):
        self.main_canvas = tk.Canvas(self, bg=self.color_bg, highlightthickness=0)
        self.main_canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_tv_background()
        self.bind("<Configure>", self.on_resize)

    def draw_tv_background(self):
        self.main_canvas.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 100: return

        cx, cy = w / 2, h / 2
        

        tv_w, tv_h = 800, 480 
        self.main_canvas.create_rectangle(cx-tv_w/2-10, cy-tv_h/2-10, cx+tv_w/2+10, cy+tv_h/2+20, fill="#333", outline="#555", width=3) 
        self.main_canvas.create_rectangle(cx-tv_w/2, cy-tv_h/2, cx+tv_w/2, cy+tv_h/2, fill="#000", outline="#222") 


        self.main_canvas.create_text(cx, cy - 30, text="CỬA HÀNG TI VI", font=("Segoe UI", 60, "bold"), fill=self.color_accent)
        self.main_canvas.create_text(cx, cy + 50, text="Công nghệ đỉnh cao - Hình ảnh sắc nét", font=("Segoe UI", 22), fill="#AAA")
        self.main_canvas.create_text(cx, cy + 100, text="DPM215465 - Lê Quốc Hùng", font=("Segoe UI", 16), fill="#666")


        if self.role == 'customer':
             btn_w, btn_h = 260, 70
             bx1, by1 = cx - btn_w/2, cy + 150
             bx2, by2 = cx + btn_w/2, cy + 150 + btn_h
             self.main_canvas.create_rectangle(bx1, by1, bx2, by2, fill="#FF5722", outline="white", width=2, tags="btn")
             self.main_canvas.create_text(cx, cy + 150 + btn_h/2, text="BẮT ĐẦU MUA SẮM", font=("Segoe UI", 16, "bold"), fill="white", tags="btn")
             self.main_canvas.tag_bind("btn", "<Button-1>", lambda e: self.mo_quan_ly_tivi())
             self.main_canvas.tag_bind("btn", "<Enter>", lambda e: self.main_canvas.config(cursor="hand2"))
             self.main_canvas.tag_bind("btn", "<Leave>", lambda e: self.main_canvas.config(cursor=""))

    def on_resize(self, event):
        self.draw_tv_background()


    def tim_kiem_nhanh(self):
        keyword = self.ent_search.get().strip()
        if not keyword:
            messagebox.showinfo("Thông báo", "Vui lòng nhập từ khóa để tìm kiếm!")
            return
        self.mo_quan_ly_tivi()
        messagebox.showinfo("Kết quả tìm kiếm", f"Đang tìm kiếm sản phẩm: '{keyword}'...\n(Chức năng lọc chi tiết đang cập nhật)")


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

    def mo_quan_ly_tivi(self): self.mo_form_chung('tivi', "Sản Phẩm", "950x650", ui_tivi.QuanLyTivi, role=self.role, callback_mua=self.mo_quan_ly_hoa_don)
    def mo_quan_ly_khach_hang(self): self.mo_form_chung('khachhang', "Khách Hàng", "950x650", ui_khachhang.QuanLyKhachHang)
    def mo_quan_ly_nhan_vien(self): self.mo_form_chung('nhanvien', "Nhân Viên", "900x600", ui_nhanvien.QuanLyNhanVien)
    def mo_quan_ly_nha_cung_cap(self): self.mo_form_chung('ncc', "Nhà Cung Cấp", "800x500", ui_nhacungcap.QuanLyNhaCungCap)
    def mo_quan_ly_hoa_don(self):
        tieu_de = "Quản Lý Hóa Đơn" if self.role == 'admin' else "Giỏ Hàng Của Tôi"
        self.mo_form_chung('hoadon', tieu_de, "1100x700", ui_hoadon.QuanLyHoaDon, role=self.role, username=self.username)


    def mo_bao_cao_hang_ton(self):
        try:
            self.mo_form_chung('baocao_ton', "Báo Cáo Hàng Tồn Kho", "1000x600", ui_baocao.BaoCaoTon)
        except NameError:
            messagebox.showwarning("Lỗi", "Không tìm thấy module 'ui_baocao'. Vui lòng kiểm tra file!")

    def mo_bao_cao_doanh_thu(self):
        try:
            self.mo_form_chung('baocao_dt', "Báo Cáo Doanh Thu", "1000x600", ui_baocao.BaoCaoDoanhThu)
        except NameError:
            messagebox.showwarning("Lỗi", "Không tìm thấy module 'ui_baocao'. Vui lòng kiểm tra file!")

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
        
        try:
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
        except Exception as e:
            messagebox.showerror("Critical Error", f"Không thể khởi chạy: {e}")