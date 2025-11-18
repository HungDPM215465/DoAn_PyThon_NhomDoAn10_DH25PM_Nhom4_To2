import tkinter as tk
from tkinter import ttk, messagebox
import database as db
import global_state

class QuanLyTivi(ttk.Frame):
    def __init__(self, parent, role='admin', callback_mua=None): 
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.role = role
        self.callback_mua = callback_mua
        self.current_action = "idle"

      
        COLOR_HEADER = "#1A237E" 
        COLOR_BG = "#F5F5F5"    
        
      
        FONT_LABEL = ("Segoe UI", 11)
        FONT_ENTRY = ("Segoe UI", 11)
        FONT_BTN = ("Segoe UI", 10, "bold")

        
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30) 
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), foreground="#333")

     
        header_frame = tk.Frame(self, bg=COLOR_HEADER, height=70)
        header_frame.pack(fill=tk.X)
        
        title_text = "QUẢN LÝ KHO TI VI" if role == 'admin' else "SIÊU THỊ TI VI - MUA SẮM ONLINE"
        icon = "🛠️" if role == 'admin' else "📺"
        
        tk.Label(header_frame, text=f"{icon} {title_text}", 
                 font=("Segoe UI", 24, "bold"), bg=COLOR_HEADER, fg="white").pack(pady=15)

       
        body_frame = tk.Frame(self, bg=COLOR_BG)
        body_frame.pack(fill=tk.BOTH, expand=True)

      
        input_frame = tk.LabelFrame(body_frame, text="Chi tiết sản phẩm", 
                                    font=("Segoe UI", 12, "bold"), bg=COLOR_BG, fg="#333", bd=2, relief="groove")
        input_frame.pack(fill=tk.X, padx=20, pady=10)

      
        def create_field(parent, label_text, row, col):
            tk.Label(parent, text=label_text, font=FONT_LABEL, bg=COLOR_BG).grid(row=row, column=col, padx=10, pady=8, sticky="w")
            entry = ttk.Entry(parent, font=FONT_ENTRY)
            entry.grid(row=row, column=col+1, padx=10, pady=8, sticky="ew")
            return entry

       
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)

      
        self.ma_tv_entry = create_field(input_frame, "Mã TV:", 0, 0)
        self.ma_tv_entry.config(state="readonly") 
        
        self.model_entry = create_field(input_frame, "Model:", 0, 2)

        
        self.ten_tv_entry = create_field(input_frame, "Tên Ti Vi:", 1, 0)
        
        tk.Label(input_frame, text="Giá bán (VNĐ):", font=FONT_LABEL, bg=COLOR_BG).grid(row=1, column=2, padx=10, sticky="w")
        self.gia_ban_entry = ttk.Entry(input_frame, font=FONT_ENTRY)
        self.gia_ban_entry.grid(row=1, column=3, padx=10, sticky="ew")

      
        tk.Label(input_frame, text="Hãng SX:", font=FONT_LABEL, bg=COLOR_BG).grid(row=2, column=0, padx=10, sticky="w")
        self.hang_sx_combo = ttk.Combobox(input_frame, values=["Sony", "Samsung", "LG", "TCL", "Panasonic", "Xiaomi", "Khác"], font=FONT_ENTRY)
        self.hang_sx_combo.grid(row=2, column=1, padx=10, sticky="ew")

        tk.Label(input_frame, text="Số lượng tồn:", font=FONT_LABEL, bg=COLOR_BG).grid(row=2, column=2, padx=10, sticky="w")
        self.so_luong_spin = ttk.Spinbox(input_frame, from_=0, to=9999, font=FONT_ENTRY)
        self.so_luong_spin.grid(row=2, column=3, padx=10, sticky="ew")


        
        btn_frame = tk.Frame(body_frame, bg=COLOR_BG)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

       
        def create_color_btn(text, cmd, bg_color, fg_color="white"):
            btn = tk.Button(btn_frame, text=text, command=cmd, 
                            bg=bg_color, fg=fg_color, font=FONT_BTN, 
                            bd=0, padx=20, pady=8, cursor="hand2", activebackground="#333", activeforeground="white")
            btn.pack(side=tk.LEFT, padx=5)
            return btn

        if self.role == 'admin':
            
            self.them_btn = create_color_btn("✚ THÊM", self.them_moi, "#2E7D32") 
            self.luu_btn = create_color_btn("💾 LƯU", self.luu, "#1565C0")     
            self.sua_btn = create_color_btn("✏️ SỬA", self.sua, "#FF8F00")    
            self.xoa_btn = create_color_btn("🗑️ XÓA", self.xoa, "#C62828")   
            self.huy_btn = create_color_btn("↩ HỦY", self.huy, "#607D8B")      

           
            self.luu_btn.config(state="disabled", bg="#B0BEC5")
            self.sua_btn.config(state="disabled", bg="#B0BEC5")
            self.huy_btn.config(state="disabled", bg="#B0BEC5")
            self.xoa_btn.config(state="disabled", bg="#B0BEC5")
        else:
          
            self.mua_btn = tk.Button(btn_frame, text="🛒 MUA NGAY", command=self.mua_ngay,
                                     bg="#FF3D00", fg="white", font=("Segoe UI", 12, "bold"),
                                     bd=0, padx=30, pady=10, cursor="hand2")
            self.mua_btn.pack(side=tk.LEFT, padx=10)

            self.gio_btn = tk.Button(btn_frame, text="➕ THÊM VÀO GIỎ", command=self.them_gio,
                                     bg="#009688", fg="white", font=("Segoe UI", 12, "bold"), 
                                     bd=0, padx=30, pady=10, cursor="hand2")
            self.gio_btn.pack(side=tk.LEFT, padx=10)
            
            self.mua_btn.config(state="disabled", bg="#B0BEC5")
            self.gio_btn.config(state="disabled", bg="#B0BEC5")

      
        tk.Button(btn_frame, text="THOÁT", command=self.thoat, bg="#424242", fg="white", font=FONT_BTN, bd=0, padx=15, pady=8).pack(side=tk.RIGHT)

      
        tree_container = tk.LabelFrame(body_frame, text="Danh sách sản phẩm hiện có", font=("Segoe UI", 12, "bold"), bg=COLOR_BG)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        columns = ('ma_tv', 'ten_tv', 'hang_sx', 'model', 'gia_ban', 'ton_kho')
        self.tree = ttk.Treeview(tree_container, columns=columns, show='headings')
        
        self.tree.heading('ma_tv', text='Mã TV'); self.tree.column('ma_tv', width=60, anchor=tk.CENTER)
        self.tree.heading('ten_tv', text='Tên Ti Vi'); self.tree.column('ten_tv', width=300)
        self.tree.heading('hang_sx', text='Hãng'); self.tree.column('hang_sx', width=100, anchor=tk.CENTER)
        self.tree.heading('model', text='Model'); self.tree.column('model', width=120, anchor=tk.CENTER)
        self.tree.heading('gia_ban', text='Giá bán (VNĐ)'); self.tree.column('gia_ban', width=150, anchor=tk.E)
        self.tree.heading('ton_kho', text='Kho'); self.tree.column('ton_kho', width=80, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        self.load_data()

   
    
    def lay_thong_tin_tv_dang_chon(self):
        selected_item_id = self.tree.focus()
        if not selected_item_id: return None
        item = self.tree.item(selected_item_id, 'values')
        gia = float(str(item[4]).replace(",", ""))
        return {'id_tv': item[0], 'ten_tv': f"{item[1]} ({item[3]})", 'don_gia': gia, 'so_luong': 1, 'thanh_tien': gia}

    def on_item_select(self, event):
        selected_item_id = self.tree.focus()
        if not selected_item_id: return
        item = self.tree.item(selected_item_id, 'values')
        self.clear_form()
        self.ma_tv_entry.config(state="normal"); self.ma_tv_entry.insert(0, item[0]); self.ma_tv_entry.config(state="readonly")
        self.ten_tv_entry.insert(0, item[1]); self.hang_sx_combo.set(item[2]); self.model_entry.insert(0, item[3])
        self.gia_ban_entry.insert(0, str(item[4]).replace(",", "")); self.so_luong_spin.set(item[5])
        
        if self.role == 'admin':
            self.sua_btn.config(state="normal", bg="#FF8F00")
            self.xoa_btn.config(state="normal", bg="#C62828")
            self.huy_btn.config(state="normal", bg="#607D8B")
            self.luu_btn.config(state="disabled", bg="#B0BEC5")
            self.them_btn.config(state="disabled", bg="#B0BEC5")
        else:
            self.mua_btn.config(state="normal", bg="#FF3D00")
            self.gio_btn.config(state="normal", bg="#009688")

    def them_gio(self):
        tv = self.lay_thong_tin_tv_dang_chon()
        if tv: global_state.gio_hang_chung.append(tv); messagebox.showinfo("Giỏ hàng", f"Đã thêm '{tv['ten_tv']}' vào giỏ!")

    def mua_ngay(self):
        tv = self.lay_thong_tin_tv_dang_chon()
        if tv: global_state.gio_hang_chung.append(tv); self.master.destroy(); self.callback_mua() if self.callback_mua else None

    def clear_form(self):
        self.ma_tv_entry.config(state="normal"); self.ma_tv_entry.delete(0, tk.END); self.ma_tv_entry.config(state="readonly")
        self.ten_tv_entry.delete(0, tk.END); self.hang_sx_combo.set(""); self.model_entry.delete(0, tk.END)
        self.gia_ban_entry.delete(0, tk.END); self.so_luong_spin.set(0); self.ten_tv_entry.focus()
    
    def reset_buttons(self):
        if self.role == 'admin':
            self.sua_btn.config(state="disabled", bg="#B0BEC5")
            self.xoa_btn.config(state="disabled", bg="#B0BEC5")
            self.huy_btn.config(state="disabled", bg="#B0BEC5")
            self.luu_btn.config(state="disabled", bg="#B0BEC5")
            self.them_btn.config(state="normal", bg="#2E7D32")
        else:
             self.mua_btn.config(state="disabled", bg="#B0BEC5")
             self.gio_btn.config(state="disabled", bg="#B0BEC5")
        self.current_action = "idle"

    def load_data(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        data = db.lay_danh_sach_tivi()
        if data:
            for item in data:
              
                gia = f"{item['gia_ban']:,.0f}"
                self.tree.insert('', tk.END, values=(item['id_tv'], item['ten_tv'], item['hang_san_xuat'], item['model'], gia, item['so_luong_ton']))

    def them_moi(self):
        self.clear_form(); self.luu_btn.config(state="normal", bg="#1565C0"); self.huy_btn.config(state="normal", bg="#607D8B"); self.them_btn.config(state="disabled", bg="#B0BEC5"); self.sua_btn.config(state="disabled", bg="#B0BEC5"); self.xoa_btn.config(state="disabled", bg="#B0BEC5"); self.current_action = "adding"
    def sua(self):
        self.luu_btn.config(state="normal", bg="#1565C0"); self.huy_btn.config(state="normal", bg="#607D8B"); self.them_btn.config(state="disabled", bg="#B0BEC5"); self.sua_btn.config(state="disabled", bg="#B0BEC5"); self.xoa_btn.config(state="disabled", bg="#B0BEC5"); self.current_action = "editing"
    def luu(self):
        try:
            ten_tv = self.ten_tv_entry.get(); hang_sx = self.hang_sx_combo.get(); model = self.model_entry.get()
            gia_ban = float(self.gia_ban_entry.get().replace(",", "")); so_luong = int(self.so_luong_spin.get()) 
        except ValueError: messagebox.showerror("Lỗi", "Giá bán và Số lượng phải là số."); return
        if not ten_tv or not hang_sx or not model: messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ Tên, Hãng, và Model."); return
        success = False
        if self.current_action == "adding": success = db.them_tivi(ten_tv, hang_sx, model, gia_ban, so_luong)
        elif self.current_action == "editing":
            try: id_tv = int(self.ma_tv_entry.get())
            except ValueError: return
            success = db.sua_tivi(id_tv, ten_tv, hang_sx, model, gia_ban, so_luong)
        if success: self.load_data(); self.clear_form(); self.reset_buttons(); messagebox.showinfo("Thông báo", "Lưu thành công!")
        else: messagebox.showerror("Lỗi", "Thao tác thất bại.")
    def huy(self):
        self.clear_form(); self.reset_buttons(); selected_item = self.tree.focus()
        if selected_item: self.tree.selection_remove(selected_item)
    def xoa(self):
        selected_item_id = self.tree.focus()
        if not selected_item_id: messagebox.showwarning("Cảnh báo", "Vui lòng chọn TV."); return
        item_values = self.tree.item(selected_item_id, 'values'); id_tv = item_values[0]; ten_tv = item_values[1]
        if messagebox.askyesno("Xác nhận", f"Xóa {ten_tv}?"):
            if db.xoa_tivi(id_tv): self.load_data(); self.clear_form(); self.reset_buttons()
            else: messagebox.showerror("Lỗi", "Không thể xóa.")
    def thoat(self):
        self.master.destroy()