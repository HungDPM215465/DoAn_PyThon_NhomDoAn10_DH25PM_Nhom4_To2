import tkinter as tk
from tkinter import ttk, messagebox
import database as db

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Đăng Nhập Hệ Thống")
        w, h = 450, 400
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f'{w}x{h}+{int((ws/2)-(w/2))}+{int((hs/2)-(h/2))}')
        self.resizable(False, False)
        self.parent = parent
        self.configure(bg="white")

       
        tk.Label(self, text="🔐 TV STORE LOGIN", font=("Segoe UI", 24, "bold"), bg="white", fg="#1565C0").pack(pady=(40, 20))

       
        frm = tk.Frame(self, bg="white")
        frm.pack(pady=10)

        def create_input(lbl):
            tk.Label(frm, text=lbl, font=("Segoe UI", 11), bg="white", fg="#555").pack(anchor="w")
            ent = ttk.Entry(frm, width=35, font=("Segoe UI", 12))
            ent.pack(pady=(0, 15))
            return ent

        self.ent_user = create_input("Tên đăng nhập")
        self.ent_user.focus()
        self.ent_pass = create_input("Mật khẩu")
        self.ent_pass.config(show="•")
        self.ent_pass.bind('<Return>', lambda e: self.dang_nhap())

       
        tk.Button(self, text="ĐĂNG NHẬP NGAY", command=self.dang_nhap, 
                  bg="#1565C0", fg="white", font=("Segoe UI", 12, "bold"), bd=0, padx=20, pady=8, cursor="hand2").pack(pady=10)

        lbl_reg = tk.Label(self, text="Chưa có tài khoản? Đăng ký tại đây", bg="white", fg="#0277BD", cursor="hand2", font=("Segoe UI", 10, "underline"))
        lbl_reg.pack(pady=5)
        lbl_reg.bind("<Button-1>", lambda e: RegisterWindow(self))

        self.login_success = False
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def dang_nhap(self):
        u = self.ent_user.get(); p = self.ent_pass.get()
        if not u or not p: messagebox.showwarning("Thiếu", "Nhập đủ thông tin!"); return
        role = db.kiem_tra_dang_nhap(u, p)
        if role:
            self.login_success = True; self.user_role = role; self.logged_user = u; self.destroy()
        else: messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")

    def on_close(self): self.login_success = False; self.destroy(); self.parent.destroy()

class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Tạo Tài Khoản")
        w, h = 400, 500
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f'{w}x{h}+{int((ws/2)-(w/2))}+{int((hs/2)-(h/2))}')
        self.configure(bg="white")

        tk.Label(self, text="📝 ĐĂNG KÝ", font=("Segoe UI", 20, "bold"), bg="white", fg="#2E7D32").pack(pady=20)
        frm = tk.Frame(self, bg="white"); frm.pack(pady=5)

        def mk_ent(txt, show=None):
            tk.Label(frm, text=txt, bg="white", font=("Segoe UI", 10)).pack(anchor="w")
            e = ttk.Entry(frm, width=30, font=("Segoe UI", 11), show=show); e.pack(pady=(0, 10))
            return e

        self.e_user = mk_ent("Tên đăng nhập:"); self.e_pass = mk_ent("Mật khẩu:", "•"); self.e_pass2 = mk_ent("Nhập lại MK:", "•")
        self.e_name = mk_ent("Họ tên:"); self.e_mail = mk_ent("Email:")

        tk.Button(self, text="HOÀN TẤT", command=self.dang_ky, bg="#2E7D32", fg="white", font=("Segoe UI", 11, "bold"), bd=0, padx=20, pady=5).pack(pady=20)

    def dang_ky(self):
        u = self.e_user.get(); p1 = self.e_pass.get(); p2 = self.e_pass2.get(); n = self.e_name.get(); m = self.e_mail.get()
        if not u or not p1: messagebox.showwarning("Lỗi", "Thiếu thông tin"); return
        if p1 != p2: messagebox.showerror("Lỗi", "Mật khẩu không khớp"); return
        if db.dang_ky_tai_khoan(u, p1, n, m): messagebox.showinfo("Xong", "Đăng ký thành công!"); self.destroy()
        else: messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại")