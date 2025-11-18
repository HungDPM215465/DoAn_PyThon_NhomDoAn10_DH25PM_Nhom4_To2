import tkinter as tk
from tkinter import ttk, messagebox
import database as db

class QuanLyKhachHang(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.current_action = "idle"

       
        COLOR_HEADER = "#6A1B9A" 
        COLOR_BG = "#F3E5F5"    
        FONT_TEXT = ("Segoe UI", 11)
        FONT_BTN = ("Segoe UI", 10, "bold")

        
        header = tk.Frame(self, bg=COLOR_HEADER, height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="💎 QUẢN LÝ KHÁCH HÀNG", font=("Segoe UI", 20, "bold"), bg=COLOR_HEADER, fg="white").pack(side=tk.LEFT, padx=20, pady=15)

      
        body = tk.Frame(self, bg=COLOR_BG)
        body.pack(fill=tk.BOTH, expand=True)

        
        input_frame = tk.LabelFrame(body, text="Thông tin khách hàng", font=("Segoe UI", 12, "bold"), bg=COLOR_BG, fg=COLOR_HEADER)
        input_frame.pack(fill=tk.X, padx=20, pady=10)

        def create_entry(lbl, r, c, width=None):
            tk.Label(input_frame, text=lbl, font=FONT_TEXT, bg=COLOR_BG).grid(row=r, column=c, padx=10, pady=8, sticky="w")
            entry = ttk.Entry(input_frame, font=FONT_TEXT, width=width)
            entry.grid(row=r, column=c+1, padx=10, pady=8, sticky="ew")
            return entry

        self.ma_kh_entry = create_entry("Mã KH:", 0, 0)
        self.ma_kh_entry.config(state="readonly")
        self.ten_kh_entry = create_entry("Họ Tên:", 0, 2)
        self.sdt_entry = create_entry("SĐT:", 1, 0)
        self.email_entry = create_entry("Email:", 1, 2)
        
        tk.Label(input_frame, text="Địa chỉ:", font=FONT_TEXT, bg=COLOR_BG).grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.dia_chi_entry = ttk.Entry(input_frame, font=FONT_TEXT)
        self.dia_chi_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=8, sticky="ew")

        input_frame.columnconfigure(1, weight=1); input_frame.columnconfigure(3, weight=1)

      
        btn_frame = tk.Frame(body, bg=COLOR_BG)
        btn_frame.pack(fill=tk.X, padx=20, pady=5)

        def mk_btn(txt, cmd, color):
            btn = tk.Button(btn_frame, text=txt, command=cmd, bg=color, fg="white", font=FONT_BTN, bd=0, padx=15, pady=8, cursor="hand2")
            btn.pack(side=tk.LEFT, padx=5)
            return btn

        self.them_btn = mk_btn("THÊM KHÁCH", self.them_moi, "#4CAF50")
        self.luu_btn = mk_btn("LƯU LẠI", self.luu, "#2196F3")
        self.sua_btn = mk_btn("SỬA TT", self.sua, "#FF9800")
        self.xoa_btn = mk_btn("XÓA KH", self.xoa, "#F44336")
        self.huy_btn = mk_btn("HỦY", self.huy, "#607D8B")
        
        self.reset_buttons()

        
        tree_frame = tk.Frame(body, bg=COLOR_BG)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        cols = ('ma_kh', 'ten_kh', 'sdt', 'email', 'dia_chi')
        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings')
        self.tree.heading('ma_kh', text='Mã KH'); self.tree.column('ma_kh', width=60, anchor="center")
        self.tree.heading('ten_kh', text='Họ Tên'); self.tree.column('ten_kh', width=180)
        self.tree.heading('sdt', text='SĐT'); self.tree.column('sdt', width=100, anchor="center")
        self.tree.heading('email', text='Email'); self.tree.column('email', width=150)
        self.tree.heading('dia_chi', text='Địa chỉ'); self.tree.column('dia_chi', width=250)
        
        scrolly = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrolly.set)
        scrolly.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        self.load_data()

    def load_data(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        for i in db.lay_danh_sach_khach_hang():
            self.tree.insert('', 'end', values=(i['id_kh'], i['ten_kh'], i['so_dien_thoai'], i['email'], i['dia_chi']))

    def on_item_select(self, event):
        sel = self.tree.focus()
        if not sel: return
        item = self.tree.item(sel, 'values')
        self.clear_form()
        self.ma_kh_entry.config(state="normal"); self.ma_kh_entry.insert(0, item[0]); self.ma_kh_entry.config(state="readonly")
        self.ten_kh_entry.insert(0, item[1]); self.sdt_entry.insert(0, item[2])
        self.email_entry.insert(0, item[3]); self.dia_chi_entry.insert(0, item[4])
        self.sua_btn.config(state="normal", bg="#FF9800"); self.xoa_btn.config(state="normal", bg="#F44336")
        self.huy_btn.config(state="normal", bg="#607D8B"); self.luu_btn.config(state="disabled", bg="#B0BEC5"); self.them_btn.config(state="disabled", bg="#B0BEC5")
        self.current_action = "idle"

    def clear_form(self):
        self.ma_kh_entry.config(state="normal"); self.ma_kh_entry.delete(0, tk.END); self.ma_kh_entry.config(state="readonly")
        self.ten_kh_entry.delete(0, tk.END); self.sdt_entry.delete(0, tk.END); self.email_entry.delete(0, tk.END); self.dia_chi_entry.delete(0, tk.END)

    def reset_buttons(self):
        self.sua_btn.config(state="disabled", bg="#B0BEC5"); self.xoa_btn.config(state="disabled", bg="#B0BEC5")
        self.huy_btn.config(state="disabled", bg="#B0BEC5"); self.luu_btn.config(state="disabled", bg="#B0BEC5")
        self.them_btn.config(state="normal", bg="#4CAF50")
        self.current_action = "idle"

    def them_moi(self): self.clear_form(); self.luu_btn.config(state="normal", bg="#2196F3"); self.huy_btn.config(state="normal", bg="#607D8B"); self.them_btn.config(state="disabled", bg="#B0BEC5"); self.sua_btn.config(state="disabled", bg="#B0BEC5"); self.xoa_btn.config(state="disabled", bg="#B0BEC5"); self.current_action = "adding"
    def sua(self): self.luu_btn.config(state="normal", bg="#2196F3"); self.huy_btn.config(state="normal", bg="#607D8B"); self.them_btn.config(state="disabled", bg="#B0BEC5"); self.sua_btn.config(state="disabled", bg="#B0BEC5"); self.xoa_btn.config(state="disabled", bg="#B0BEC5"); self.current_action = "editing"
    def huy(self): self.clear_form(); self.reset_buttons()
    def luu(self):
        ten = self.ten_kh_entry.get(); sdt = self.sdt_entry.get(); email = self.email_entry.get(); dia_chi = self.dia_chi_entry.get()
        if not ten or not sdt: messagebox.showerror("Lỗi", "Thiếu tên hoặc SĐT"); return
        if self.current_action == "adding": success = db.them_khach_hang(ten, sdt, dia_chi, email)
        else: id_kh = self.ma_kh_entry.get(); success = db.sua_khach_hang(id_kh, ten, sdt, dia_chi, email)
        if success: self.load_data(); self.clear_form(); self.reset_buttons(); messagebox.showinfo("Xong", "Lưu thành công")
        else: messagebox.showerror("Lỗi", "Thao tác thất bại")
    def xoa(self):
        sel = self.tree.focus()
        if not sel: return
        item = self.tree.item(sel, 'values')
        if messagebox.askyesno("Xóa", f"Xóa khách {item[1]}?"):
            if db.xoa_khach_hang(item[0]): self.load_data(); self.clear_form(); self.reset_buttons()
            else: messagebox.showerror("Lỗi", "Không thể xóa")