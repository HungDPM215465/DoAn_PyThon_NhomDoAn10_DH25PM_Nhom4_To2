import tkinter as tk
from tkinter import ttk, messagebox
import database as db

class QuanLyNhaCungCap(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.current_action = "idle"

        COLOR_HEADER = "#00695C" 
        COLOR_BG = "#E0F2F1"     
        FONT_TEXT = ("Segoe UI", 11)
        FONT_BTN = ("Segoe UI", 10, "bold")

        header = tk.Frame(self, bg=COLOR_HEADER, height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="🏭 QUẢN LÝ NHÀ CUNG CẤP", font=("Segoe UI", 20, "bold"), bg=COLOR_HEADER, fg="white").pack(side=tk.LEFT, padx=20, pady=15)

        body = tk.Frame(self, bg=COLOR_BG)
        body.pack(fill=tk.BOTH, expand=True)

     
        input_frame = tk.LabelFrame(body, text="Thông tin đối tác", font=("Segoe UI", 12, "bold"), bg=COLOR_BG, fg=COLOR_HEADER)
        input_frame.pack(fill=tk.X, padx=20, pady=10)

        def make_entry(txt, r, c):
            tk.Label(input_frame, text=txt, font=FONT_TEXT, bg=COLOR_BG).grid(row=r, column=c, padx=10, pady=8, sticky="w")
            ent = ttk.Entry(input_frame, font=FONT_TEXT)
            ent.grid(row=r, column=c+1, padx=10, pady=8, sticky="ew")
            return ent

        self.ent_ten = make_entry("Tên NCC:", 0, 0)
        self.ent_sdt = make_entry("SĐT:", 0, 2)
        self.ent_email = make_entry("Email:", 1, 0)
        self.ent_diachi = make_entry("Địa chỉ:", 1, 2)
        self.var_id = tk.StringVar()
        
        input_frame.columnconfigure(1, weight=1); input_frame.columnconfigure(3, weight=1)

      
        btn_frame = tk.Frame(body, bg=COLOR_BG)
        btn_frame.pack(fill=tk.X, padx=20, pady=5)
        
        def mk_btn(txt, cmd, clr):
            tk.Button(btn_frame, text=txt, command=cmd, bg=clr, fg="white", font=FONT_BTN, bd=0, padx=15, pady=8, cursor="hand2").pack(side=tk.LEFT, padx=5)

        mk_btn("THÊM", self.them, "#00897B")
        mk_btn("LƯU", self.luu, "#0277BD")
        mk_btn("XÓA", self.xoa, "#C62828")

      
        tree_frame = tk.Frame(body, bg=COLOR_BG)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        cols = ("ID", "Tên", "Địa chỉ", "SĐT", "Email")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c)
        self.tree.column("ID", width=40, anchor="center")
        
        scrolly = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrolly.set)
        scrolly.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        self.tree.bind("<<TreeviewSelect>>", self.chon_dong)
        self.load_data()

    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in db.lay_danh_sach_ncc():
            self.tree.insert("", "end", values=(r['id_ncc'], r['ten_ncc'], r['dia_chi'], r['so_dien_thoai'], r['email']))

    def chon_dong(self, event):
        sel = self.tree.focus()
        if not sel: return
        val = self.tree.item(sel, "values")
        self.var_id.set(val[0])
        self.ent_ten.delete(0, tk.END); self.ent_ten.insert(0, val[1])
        self.ent_diachi.delete(0, tk.END); self.ent_diachi.insert(0, val[2])
        self.ent_sdt.delete(0, tk.END); self.ent_sdt.insert(0, val[3])
        self.ent_email.delete(0, tk.END); self.ent_email.insert(0, val[4])
        self.current_action = "editing"

    def them(self):
        self.ent_ten.delete(0, tk.END); self.ent_diachi.delete(0, tk.END); self.ent_sdt.delete(0, tk.END); self.ent_email.delete(0, tk.END)
        self.current_action = "adding"; self.ent_ten.focus()

    def luu(self):
        if self.current_action == "adding": db.them_ncc(self.ent_ten.get(), self.ent_diachi.get(), self.ent_sdt.get(), self.ent_email.get())
        elif self.current_action == "editing": db.sua_ncc(self.var_id.get(), self.ent_ten.get(), self.ent_diachi.get(), self.ent_sdt.get(), self.ent_email.get())
        self.load_data(); self.them()

    def xoa(self):
        if not self.var_id.get(): return
        if messagebox.askyesno("Xóa", "Bạn chắc chứ?"): db.xoa_ncc(self.var_id.get()); self.load_data(); self.them()