import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import database as db
from datetime import datetime
import global_state

class QuanLyHoaDon(ttk.Frame):
    def __init__(self, parent, role='admin', username='admin'):
        super().__init__(parent, padding="10")
        self.pack(fill=tk.BOTH, expand=True)
        
        self.role = role
        self.username = username

     
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

       
        title_tab1 = "Lập Hóa Đơn Mới" if role == 'admin' else "Giỏ Hàng & Thanh Toán"
        self.tab_tao = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_tao, text=title_tab1)
        self.setup_tab_tao()

       
        if self.role == 'admin':
            self.tab_lichsu = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(self.tab_lichsu, text="Quản Lý Lịch Sử Hóa Đơn")
            self.setup_tab_lichsu()

 
    def setup_tab_tao(self):
        
        frame_top = ttk.LabelFrame(self.tab_tao, text="Thông tin khách hàng")
        frame_top.pack(fill=tk.X, pady=5)
        
        if self.role == 'admin':
            
            ttk.Label(frame_top, text="Chọn Khách hàng:").pack(side=tk.LEFT, padx=5)
            self.cbo_khach = ttk.Combobox(frame_top, width=30, state="readonly")
            self.cbo_khach.pack(side=tk.LEFT, padx=5, pady=10)
            ttk.Button(frame_top, text="Tải lại DS", command=self.load_combobox_data).pack(side=tk.LEFT, padx=5)
        else:
           
            lbl_hello = ttk.Label(frame_top, text=f"Xin chào: {self.username}", 
                                  font=("Arial", 12, "bold"), foreground="green")
            lbl_hello.pack(side=tk.LEFT, padx=10, pady=10)
            
          
            self.id_kh_hien_tai = self.lay_id_khach_hang_tu_user(self.username)
            if not self.id_kh_hien_tai:
                ttk.Label(frame_top, text="(Lần đầu mua sắm - Hệ thống sẽ tự tạo hồ sơ)", foreground="gray").pack(side=tk.LEFT)

        
        frame_add = ttk.LabelFrame(self.tab_tao, text="Thêm sản phẩm thủ công")
        frame_add.pack(fill=tk.X, pady=5)

        ttk.Label(frame_add, text="Sản phẩm:").grid(row=0, column=0, padx=5, pady=5)
        self.cbo_tivi = ttk.Combobox(frame_add, width=35, state="readonly")
        self.cbo_tivi.grid(row=0, column=1, padx=5)
        self.cbo_tivi.bind("<<ComboboxSelected>>", self.on_tivi_select)

        ttk.Label(frame_add, text="Giá:").grid(row=0, column=2, padx=5)
        self.lbl_gia = ttk.Label(frame_add, text="0", foreground="red", font=("Arial", 10, "bold"))
        self.lbl_gia.grid(row=0, column=3, padx=5)

        ttk.Label(frame_add, text="SL:").grid(row=0, column=4, padx=5)
        self.spin_sl = ttk.Spinbox(frame_add, from_=1, to=100, width=5)
        self.spin_sl.set(1)
        self.spin_sl.grid(row=0, column=5, padx=5)

        ttk.Button(frame_add, text="Thêm", command=self.them_vao_gio).grid(row=0, column=6, padx=10)

       
        frame_cart = ttk.LabelFrame(self.tab_tao, text="Giỏ hàng cần thanh toán")
        frame_cart.pack(fill=tk.BOTH, expand=True, pady=5)

        cols = ("ID_TV", "Tên TV", "Đơn giá", "Số lượng", "Thành tiền")
        self.tree_cart = ttk.Treeview(frame_cart, columns=cols, show="headings", height=8)
        
        self.tree_cart.heading("ID_TV", text="Mã"); self.tree_cart.column("ID_TV", width=50, anchor="center")
        self.tree_cart.heading("Tên TV", text="Tên Sản Phẩm"); self.tree_cart.column("Tên TV", width=300)
        self.tree_cart.heading("Đơn giá", text="Đơn giá"); self.tree_cart.column("Đơn giá", width=100, anchor="e")
        self.tree_cart.heading("Số lượng", text="SL"); self.tree_cart.column("Số lượng", width=50, anchor="center")
        self.tree_cart.heading("Thành tiền", text="Thành tiền"); self.tree_cart.column("Thành tiền", width=120, anchor="e")
        
        self.tree_cart.pack(fill=tk.BOTH, expand=True)

     
        frame_bottom = ttk.Frame(self.tab_tao)
        frame_bottom.pack(fill=tk.X, pady=10)

        self.lbl_tongtien = ttk.Label(frame_bottom, text="TỔNG TIỀN: 0 VNĐ", font=("Arial", 16, "bold"), foreground="red")
        self.lbl_tongtien.pack(side=tk.RIGHT, padx=20)

        btn_text = "XÁC NHẬN THANH TOÁN" if self.role == 'customer' else "LƯU HÓA ĐƠN"
        btn_color = "#FF5722" if self.role == 'customer' else "#2196F3" 
        
       
        self.btn_pay = tk.Button(frame_bottom, text=btn_text, font=("Arial", 12, "bold"), 
                                 bg=btn_color, fg="white", padx=20, pady=5, command=self.thanh_toan)
        self.btn_pay.pack(side=tk.RIGHT)

        ttk.Button(frame_bottom, text="Xóa dòng chọn", command=self.xoa_khoi_gio).pack(side=tk.LEFT)

       
        self.gio_hang = []
        self.map_kh = {}
        self.map_tv = {}
        
        self.load_combobox_data()
        
        self.nap_tu_global_state()

    def lay_id_khach_hang_tu_user(self, username):
        """Tìm xem user này đã có hồ sơ trong bảng khach_hang chưa"""
      
        conn = db.create_connection()
        cursor = conn.cursor()
       
        cursor.execute("SELECT id_kh FROM khach_hang WHERE email LIKE ?", (f"%{username}%",))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def nap_tu_global_state(self):
        if global_state.gio_hang_chung:
            for item in global_state.gio_hang_chung:
                self.gio_hang.append(item)
                self.tree_cart.insert("", "end", values=(
                    item['id_tv'], item['ten_tv'], 
                    f"{item['don_gia']:,.0f}", item['so_luong'], 
                    f"{item['thanh_tien']:,.0f}"
                ))
            self.cap_nhat_tong_tien()

    def load_combobox_data(self):
        
        self.map_tv = {}
        tv_list = []
        for tv in db.lay_danh_sach_tivi():
            label = f"{tv['ten_tv']} ({tv['model']})"
            self.map_tv[label] = {'id': tv['id_tv'], 'gia': tv['gia_ban'], 'ton': tv['so_luong_ton']}
            tv_list.append(label)
        self.cbo_tivi['values'] = tv_list

       
        if self.role == 'admin':
            self.map_kh = {}
            kh_list = []
            for kh in db.lay_danh_sach_khach_hang():
                label = f"{kh['ten_kh']} - {kh['so_dien_thoai']}"
                self.map_kh[label] = kh['id_kh']
                kh_list.append(label)
            self.cbo_khach['values'] = kh_list

    def on_tivi_select(self, event):
        name = self.cbo_tivi.get()
        if name in self.map_tv:
            info = self.map_tv[name]
            self.lbl_gia.config(text=f"{info['gia']:,.0f}")

    def them_vao_gio(self):
        name = self.cbo_tivi.get()
        if not name: return
        try: sl = int(self.spin_sl.get())
        except: return
        
        info = self.map_tv[name]
        if sl > info['ton']:
            messagebox.showwarning("Kho", "Không đủ hàng!")
            return
            
        thanh_tien = sl * info['gia']
        item = {'id_tv': info['id'], 'ten_tv': name, 'don_gia': info['gia'], 'so_luong': sl, 'thanh_tien': thanh_tien}
        self.gio_hang.append(item)
        self.tree_cart.insert("", "end", values=(info['id'], name, f"{info['gia']:,.0f}", sl, f"{thanh_tien:,.0f}"))
        self.cap_nhat_tong_tien()

    def xoa_khoi_gio(self):
        sel = self.tree_cart.selection()
        if sel:
            idx = self.tree_cart.index(sel[0])
            del self.gio_hang[idx]
            self.tree_cart.delete(sel)
            self.cap_nhat_tong_tien()
            global_state.gio_hang_chung = self.gio_hang

    def cap_nhat_tong_tien(self):
        total = sum(item['thanh_tien'] for item in self.gio_hang)
        self.lbl_tongtien.config(text=f"TỔNG TIỀN: {total:,.0f} VNĐ")

    def thanh_toan(self):
        if not self.gio_hang:
            messagebox.showwarning("Giỏ trống", "Vui lòng mua thêm sản phẩm!")
            return

        id_kh_thanh_toan = None

        if self.role == 'admin':
          
            kh_text = self.cbo_khach.get()
            if not kh_text:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn khách hàng!")
                return
            id_kh_thanh_toan = self.map_kh[kh_text]
        else:
            
            if self.id_kh_hien_tai:
                id_kh_thanh_toan = self.id_kh_hien_tai
            else:
               
                db.them_khach_hang(self.username, "0000000000", "Địa chỉ Online", self.username + "@email.com")
                
                all_kh = db.lay_danh_sach_khach_hang()
                id_kh_thanh_toan = all_kh[-1]['id_kh'] 

        if messagebox.askyesno("Xác nhận", "Bạn muốn thanh toán đơn hàng này?"):
            if db.tao_hoa_don_moi(id_kh_thanh_toan, self.gio_hang):
                if self.role == 'customer':
                    messagebox.showinfo("Cảm ơn", "Đặt hàng thành công!\nCửa hàng sẽ sớm liên hệ bạn.")
                else:
                    messagebox.showinfo("Thành công", "Đã lưu hóa đơn.")
                
               
                self.gio_hang = []
                global_state.gio_hang_chung = []
                for row in self.tree_cart.get_children(): self.tree_cart.delete(row)
                self.cap_nhat_tong_tien()
                self.load_combobox_data()
                if self.role == 'admin': self.load_lich_su()
            else:
                messagebox.showerror("Lỗi", "Lỗi hệ thống CSDL.")

  
    def setup_tab_lichsu(self):
        paned = ttk.PanedWindow(self.tab_lichsu, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        frame_left = ttk.LabelFrame(paned, text="Danh sách Hóa Đơn")
        paned.add(frame_left, weight=1)
        
        cols_hd = ("ID", "Khách hàng", "Ngày lập", "Tổng tiền")
        self.tree_hd = ttk.Treeview(frame_left, columns=cols_hd, show="headings")
        for c in cols_hd: self.tree_hd.heading(c, text=c)
        self.tree_hd.column("ID", width=50, anchor="center")
        self.tree_hd.column("Tổng tiền", anchor="e")
        self.tree_hd.pack(fill=tk.BOTH, expand=True)
        self.tree_hd.bind("<<TreeviewSelect>>", self.on_hoadon_select)
        
        ttk.Button(frame_left, text="Làm mới", command=self.load_lich_su).pack(pady=5)

        frame_right = ttk.LabelFrame(paned, text="Chi tiết hóa đơn")
        paned.add(frame_right, weight=2)
        
        cols_ct = ("Tên TV", "SL", "Đơn giá", "Thành tiền")
        self.tree_ct = ttk.Treeview(frame_right, columns=cols_ct, show="headings")
        for c in cols_ct: self.tree_ct.heading(c, text=c)
        self.tree_ct.column("SL", width=50, anchor="center")
        self.tree_ct.column("Đơn giá", anchor="e")
        self.tree_ct.column("Thành tiền", anchor="e")
        self.tree_ct.pack(fill=tk.BOTH, expand=True)
        
        self.load_lich_su()

    def load_lich_su(self):
        for r in self.tree_hd.get_children(): self.tree_hd.delete(r)
        for hd in db.lay_danh_sach_hoa_don():
            ngay = hd['ngay_lap'].strftime("%d/%m/%Y %H:%M") if hd['ngay_lap'] else ""
            self.tree_hd.insert("", "end", values=(hd['id_hd'], hd['ten_kh'], ngay, f"{hd['tong_tien']:,.0f}"))

    def on_hoadon_select(self, event):
        sel = self.tree_hd.focus()
        if not sel: return
        id_hd = self.tree_hd.item(sel, "values")[0]
        for r in self.tree_ct.get_children(): self.tree_ct.delete(r)
        for ct in db.lay_chi_tiet_hoa_don(id_hd):
            self.tree_ct.insert("", "end", values=(ct['ten_tv'], ct['so_luong'], f"{ct['don_gia_luc_ban']:,.0f}", f"{ct['thanh_tien']:,.0f}"))