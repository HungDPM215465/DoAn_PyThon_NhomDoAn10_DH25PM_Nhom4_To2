import tkinter as tk
from tkinter import ttk, messagebox
import database as db

class QuanLyNhanVien(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.current_action = "idle"

        
        COLOR_HEADER = "#EF6C00"
        COLOR_BG = "#FAFAFA"  
        
        FONT_LABEL = ("Segoe UI", 11)
        FONT_ENTRY = ("Segoe UI", 11)
        FONT_BTN = ("Segoe UI", 10, "bold")

       
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), foreground="#333")

     
        header_frame = tk.Frame(self, bg=COLOR_HEADER, height=70)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="👥 QUẢN LÝ NHÂN SỰ", 
                 font=("Segoe UI", 22, "bold"), bg=COLOR_HEADER, fg="white").pack(side=tk.LEFT, padx=20, pady=15)

        
        body_frame = tk.Frame(self, bg=COLOR_BG)
        body_frame.pack(fill=tk.BOTH, expand=True)

      
        input_frame = tk.LabelFrame(body_frame, text="Hồ sơ nhân viên", 
                                    font=("Segoe UI", 12, "bold"), bg=COLOR_BG, fg="#EF6C00", bd=2, relief="groove")
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
      
        def create_field(lbl_text, r, c, width=None):
            tk.Label(input_frame, text=lbl_text, font=FONT_LABEL, bg=COLOR_BG).grid(row=r, column=c, padx=10, pady=10, sticky="w")
            entry = ttk.Entry(input_frame, font=FONT_ENTRY, width=width)
            entry.grid(row=r, column=c+1, padx=10, pady=10, sticky="ew")
            return entry

        
        self.ent_ma = create_field("Mã số:", 0, 0)
        self.ent_ma.config(state="readonly")

        tk.Label(input_frame, text="Chức vụ:", font=FONT_LABEL, bg=COLOR_BG).grid(row=0, column=2, padx=10, sticky="w")
        self.cbo_chucvu = ttk.Combobox(input_frame, values=["Trưởng phòng", "Phó phòng", "Nhân viên", "Kế toán", "Bảo vệ"], font=FONT_ENTRY)
        self.cbo_chucvu.grid(row=0, column=3, padx=10, sticky="ew")

       
        self.ent_ho = create_field("Họ lót:", 1, 0)
        self.ent_ten = create_field("Tên:", 1, 2)

        
        tk.Label(input_frame, text="Giới tính:", font=FONT_LABEL, bg=COLOR_BG).grid(row=2, column=0, padx=10, sticky="w")
        
        f_phai = tk.Frame(input_frame, bg=COLOR_BG)
        f_phai.grid(row=2, column=1, padx=10, sticky="w")
        self.var_phai = tk.StringVar(value="Nam")
        
       
        style.configure("TRadiobutton", background=COLOR_BG, font=FONT_LABEL)
        ttk.Radiobutton(f_phai, text="Nam", variable=self.var_phai, value="Nam").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(f_phai, text="Nữ", variable=self.var_phai, value="Nữ").pack(side=tk.LEFT, padx=5)

        self.ent_ngaysinh = create_field("Ngày sinh (yyyy-mm-dd):", 2, 2)

        self.var_id_sql = tk.StringVar()

       
        btn_frame = tk.Frame(body_frame, bg=COLOR_BG)
        btn_frame.pack(fill=tk.X, padx=20, pady=5)

        def create_btn(text, cmd, bg_color):
            btn = tk.Button(btn_frame, text=text, command=cmd, bg=bg_color, fg="white", 
                            font=FONT_BTN, bd=0, padx=20, pady=8, cursor="hand2", activebackground="#333", activeforeground="white")
            btn.pack(side=tk.LEFT, padx=5)
            return btn

        self.btn_them = create_btn("✚ THÊM MỚI", self.them, "#43A047") 
        self.btn_luu = create_btn("💾 LƯU LẠI", self.luu, "#1976D2") 
        self.btn_xoa = create_btn("🗑️ XÓA NV", self.xoa, "#D32F2F")   
        self.btn_huy = create_btn("↩ HỦY", self.huy, "#607D8B")      

        tk.Button(btn_frame, text="THOÁT", command=self.thoat, bg="#424242", fg="white", 
                  font=FONT_BTN, bd=0, padx=15, pady=8).pack(side=tk.RIGHT, padx=5)

      
        self.reset_buttons()

    
        tree_container = tk.LabelFrame(body_frame, text="Danh sách nhân viên", font=("Segoe UI", 12, "bold"), bg=COLOR_BG)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))

        cols = ("Mã số", "Họ lót", "Tên", "Phái", "Ngày sinh", "Chức vụ")
        self.tree = ttk.Treeview(tree_container, columns=cols, show="headings")
        
        self.tree.heading("Mã số", text="Mã NV"); self.tree.column("Mã số", width=80, anchor="center")
        self.tree.heading("Họ lót", text="Họ đệm"); self.tree.column("Họ lót", width=150)
        self.tree.heading("Tên", text="Tên"); self.tree.column("Tên", width=100)
        self.tree.heading("Phái", text="Giới tính"); self.tree.column("Phái", width=80, anchor="center")
        self.tree.heading("Ngày sinh", text="Ngày sinh"); self.tree.column("Ngày sinh", width=120, anchor="center")
        self.tree.heading("Chức vụ", text="Chức vụ"); self.tree.column("Chức vụ", width=150)

        scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.chon_dong)
        self.load_data()

    

    def reset_buttons(self):
        """Đặt lại trạng thái nút"""
        self.btn_them.config(state="normal", bg="#43A047")
        self.btn_luu.config(state="disabled", bg="#B0BEC5")
        self.btn_xoa.config(state="disabled", bg="#B0BEC5")
        self.btn_huy.config(state="disabled", bg="#B0BEC5")
        self.current_action = "idle"

    def clear_form(self):
        self.ent_ma.config(state="normal"); self.ent_ma.delete(0, tk.END); self.ent_ma.config(state="readonly")
        self.ent_ho.delete(0, tk.END)
        self.ent_ten.delete(0, tk.END)
        self.ent_ngaysinh.delete(0, tk.END)
        self.cbo_chucvu.set("")
        self.var_phai.set("Nam")
        self.ent_ho.focus()

    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        data = db.lay_danh_sach_nv()
        if data:
            for r in data:
                self.tree.insert("", "end", iid=r['id_nv'], values=(r['ma_nv'], r['ho_lot'], r['ten'], r['gioi_tinh'], r['ngay_sinh'], r['chuc_vu']))

    def chon_dong(self, event):
        sel_id = self.tree.focus()
        if not sel_id: return
        val = self.tree.item(sel_id, "values")
        
        self.var_id_sql.set(sel_id)
        self.ent_ma.config(state="normal"); self.ent_ma.delete(0, tk.END); self.ent_ma.insert(0, val[0]); self.ent_ma.config(state="readonly")
        self.ent_ho.delete(0, tk.END); self.ent_ho.insert(0, val[1])
        self.ent_ten.delete(0, tk.END); self.ent_ten.insert(0, val[2])
        self.var_phai.set(val[3])
        self.ent_ngaysinh.delete(0, tk.END); self.ent_ngaysinh.insert(0, val[4])
        self.cbo_chucvu.set(val[5])
        self.current_action = "editing"

       
        self.btn_luu.config(state="normal", bg="#1976D2", text="💾 CẬP NHẬT")
        self.btn_xoa.config(state="normal", bg="#D32F2F")
        self.btn_huy.config(state="normal", bg="#607D8B")
        self.btn_them.config(state="disabled", bg="#B0BEC5")

    def them(self):
        self.clear_form()
        self.current_action = "adding"
       
        self.btn_luu.config(state="normal", bg="#1976D2", text="💾 LƯU MỚI")
        self.btn_huy.config(state="normal", bg="#607D8B")
        self.btn_them.config(state="disabled", bg="#B0BEC5")
        self.btn_xoa.config(state="disabled", bg="#B0BEC5")

    def luu(self):
        if not self.ent_ho.get() or not self.ent_ten.get():
            messagebox.showerror("Lỗi", "Vui lòng nhập tên nhân viên!")
            return

        if self.current_action == "adding":
            db.them_nv(self.ent_ho.get(), self.ent_ten.get(), self.var_phai.get(), self.ent_ngaysinh.get(), self.cbo_chucvu.get())
        elif self.current_action == "editing":
            db.sua_nv(self.var_id_sql.get(), self.ent_ho.get(), self.ent_ten.get(), self.var_phai.get(), self.ent_ngaysinh.get(), self.cbo_chucvu.get())
        
        self.load_data()
        self.clear_form()
        self.reset_buttons()
        messagebox.showinfo("Thành công", "Đã lưu dữ liệu nhân viên!")

    def xoa(self):
        if not self.var_id_sql.get(): return
        if messagebox.askyesno("Xóa", "Bạn có chắc muốn xóa nhân viên này không?"):
            db.xoa_nv(self.var_id_sql.get())
            self.load_data()
            self.clear_form()
            self.reset_buttons()

    def huy(self):
        self.clear_form()
        self.reset_buttons()
    
        sel = self.tree.focus()
        if sel: self.tree.selection_remove(sel)

    def thoat(self):
        self.master.destroy()