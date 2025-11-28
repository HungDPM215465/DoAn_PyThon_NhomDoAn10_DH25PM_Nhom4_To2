import tkinter as tk
from tkinter import ttk, messagebox
import database as db

class BaoCaoTon(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.parent = parent
        
        # --- TIÊU ĐỀ ---
        lbl_title = tk.Label(self, text="BÁO CÁO HÀNG TỒN KHO", font=("Segoe UI", 24, "bold"), fg="#0078D7")
        lbl_title.pack(pady=20)

        # --- THANH CÔNG CỤ / LỌC ---
        frame_tools = tk.Frame(self)
        frame_tools.pack(fill=tk.X, padx=20, pady=10)

        btn_refresh = tk.Button(frame_tools, text="🔄 Làm mới dữ liệu", font=("Segoe UI", 11), bg="#4CAF50", fg="white", command=self.load_data)
        btn_refresh.pack(side=tk.LEFT)
        
        btn_export = tk.Button(frame_tools, text="📂 Xuất Excel", font=("Segoe UI", 11), bg="#2196F3", fg="white", command=self.xuat_excel)
        btn_export.pack(side=tk.RIGHT)

        # --- BẢNG DỮ LIỆU (TREEVIEW) ---
        columns = ("ID", "TenTV", "Loai", "HangSX", "GiaNhap", "GiaBan", "SoLuongTon", "TrangThai")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=20)
        
        # Cấu hình cột
        self.tree.heading("ID", text="Mã TV")
        self.tree.column("ID", width=80, anchor=tk.CENTER)
        
        self.tree.heading("TenTV", text="Tên Ti Vi")
        self.tree.column("TenTV", width=250)
        
        self.tree.heading("Loai", text="Loại")
        self.tree.column("Loai", width=100, anchor=tk.CENTER)

        self.tree.heading("HangSX", text="Hãng SX")
        self.tree.column("HangSX", width=100, anchor=tk.CENTER)

        self.tree.heading("GiaNhap", text="Giá Nhập")
        self.tree.column("GiaNhap", width=120, anchor=tk.E)

        self.tree.heading("GiaBan", text="Giá Bán")
        self.tree.column("GiaBan", width=120, anchor=tk.E)

        self.tree.heading("SoLuongTon", text="Tồn Kho")
        self.tree.column("SoLuongTon", width=100, anchor=tk.CENTER)

        self.tree.heading("TrangThai", text="Cảnh báo")
        self.tree.column("TrangThai", width=150, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Load dữ liệu khi mở
        self.load_data()

    def load_data(self):
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = db.create_connection()
        if conn:
            try:
                cur = conn.cursor()
                # Giả sử bảng tên là 'tivi'
                cur.execute("SELECT MaTV, TenTV, LoaiTV, HangSX, GiaNhap, GiaBan, SoLuong FROM tivi ORDER BY SoLuong ASC")
                rows = cur.fetchall()
                
                total_ton = 0
                total_value = 0

                for row in rows:
                    ma, ten, loai, hang, gianhap, giaban, sluong = row
                    
                    # Logic cảnh báo tồn kho
                    trang_thai = "✅ Ổn định"
                    tag = "normal"
                    if sluong == 0:
                        trang_thai = "⛔ HẾT HÀNG"
                        tag = "het_hang"
                    elif sluong < 5:
                        trang_thai = "⚠️ Sắp hết"
                        tag = "sap_het"
                    
                    self.tree.insert("", tk.END, values=(ma, ten, loai, hang, f"{gianhap:,.0f}", f"{giaban:,.0f}", sluong, trang_thai), tags=(tag,))
                    
                    total_ton += sluong
                    total_value += (gianhap * sluong)

                # Tô màu
                self.tree.tag_configure("het_hang", foreground="red", background="#FFEBEE")
                self.tree.tag_configure("sap_het", foreground="#F57C00", background="#FFF3E0")

                # Label tổng kết chân trang
                lbl_footer = tk.Label(self, text=f"Tổng số lượng tồn: {total_ton} sản phẩm  |  Tổng giá trị tồn kho: {total_value:,.0f} VNĐ", 
                                      font=("Segoe UI", 12, "bold"), bg="#EEE", pady=10)
                lbl_footer.pack(fill=tk.X, side=tk.BOTTOM)

            except Exception as e:
                # Nếu chưa có DB thì hiển thị dữ liệu mẫu để test giao diện
                # messagebox.showerror("Lỗi DB", str(e))
                self.tree.insert("", tk.END, values=("TV001", "Sony Bravia 4K (Demo)", "4K", "Sony", "10,000,000", "12,000,000", 2, "⚠️ Sắp hết"), tags=("sap_het",))
                self.tree.insert("", tk.END, values=("TV002", "Samsung QLED (Demo)", "QLED", "Samsung", "15,000,000", "18,000,000", 0, "⛔ HẾT HÀNG"), tags=("het_hang",))
                self.tree.insert("", tk.END, values=("TV003", "LG OLED (Demo)", "OLED", "LG", "20,000,000", "25,000,000", 15, "✅ Ổn định"))
            finally:
                conn.close()

    def xuat_excel(self):
        messagebox.showinfo("Thông báo", "Chức năng xuất ra file Excel đang phát triển!")


class BaoCaoDoanhThu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        
        # --- TIÊU ĐỀ ---
        lbl_title = tk.Label(self, text="BÁO CÁO DOANH THU", font=("Segoe UI", 24, "bold"), fg="#D32F2F")
        lbl_title.pack(pady=20)

        # --- BỘ LỌC NGÀY THÁNG ---
        frame_filter = tk.LabelFrame(self, text="Bộ lọc thời gian", font=("Segoe UI", 10))
        frame_filter.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(frame_filter, text="Từ ngày (YYYY-MM-DD):").pack(side=tk.LEFT, padx=10, pady=10)
        self.ent_from = tk.Entry(frame_filter, width=15)
        self.ent_from.pack(side=tk.LEFT, padx=5)
        self.ent_from.insert(0, "2023-01-01") # Mặc định

        tk.Label(frame_filter, text="Đến ngày:").pack(side=tk.LEFT, padx=10)
        self.ent_to = tk.Entry(frame_filter, width=15)
        self.ent_to.pack(side=tk.LEFT, padx=5)
        self.ent_to.insert(0, "2025-12-31") # Mặc định

        btn_thongke = tk.Button(frame_filter, text="📊 Xem Báo Cáo", bg="#D32F2F", fg="white", font=("Segoe UI", 10, "bold"), command=self.thong_ke)
        btn_thongke.pack(side=tk.LEFT, padx=20)

        # --- BẢNG DỮ LIỆU ---
        columns = ("Ngay", "SoDonHang", "DoanhThu", "LoiNhuan")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=18)
        
        self.tree.heading("Ngay", text="Ngày")
        self.tree.column("Ngay", width=150, anchor=tk.CENTER)

        self.tree.heading("SoDonHang", text="Số Đơn Hàng")
        self.tree.column("SoDonHang", width=150, anchor=tk.CENTER)

        self.tree.heading("DoanhThu", text="Doanh Thu (VNĐ)")
        self.tree.column("DoanhThu", width=200, anchor=tk.E)

        self.tree.heading("LoiNhuan", text="Lợi Nhuận Ước Tính (VNĐ)")
        self.tree.column("LoiNhuan", width=200, anchor=tk.E)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Khu vực tổng kết
        self.lbl_total = tk.Label(self, text="Tổng doanh thu: 0 VNĐ", font=("Segoe UI", 14, "bold"), fg="#D32F2F")
        self.lbl_total.pack(pady=10)

    def thong_ke(self):
        # Xóa cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        ngay_bd = self.ent_from.get()
        ngay_kt = self.ent_to.get()

        conn = db.create_connection()
        if conn:
            try:
                cur = conn.cursor()
                # Query giả định: Tính tổng tiền theo ngày từ bảng hoadon
                # Lưu ý: Cần bảng hoadon có cột NgayLap và TongTien
                sql = """
                    SELECT NgayLap, COUNT(*), SUM(TongTien) 
                    FROM hoadon 
                    WHERE NgayLap BETWEEN %s AND %s 
                    GROUP BY NgayLap 
                    ORDER BY NgayLap DESC
                """
                cur.execute(sql, (ngay_bd, ngay_kt))
                rows = cur.fetchall()
                
                total_dt = 0
                for row in rows:
                    ngay, count, sum_tien = row
                    loi_nhuan = sum_tien * 0.2 # Giả định lợi nhuận 20%
                    self.tree.insert("", tk.END, values=(ngay, count, f"{sum_tien:,.0f}", f"{loi_nhuan:,.0f}"))
                    total_dt += sum_tien
                
                self.lbl_total.config(text=f"Tổng doanh thu: {total_dt:,.0f} VNĐ")
            
            except Exception as e:
                # Dữ liệu mẫu nếu query lỗi
                self.tree.insert("", tk.END, values=("2023-11-20", 5, "150,000,000", "30,000,000"))
                self.tree.insert("", tk.END, values=("2023-11-21", 3, "85,000,000", "17,000,000"))
                self.lbl_total.config(text=f"Tổng doanh thu (Demo): 235,000,000 VNĐ")
            finally:
                conn.close()
        else:
            # Demo offline
            self.tree.insert("", tk.END, values=("2023-11-20", 5, "150,000,000", "30,000,000"))
            self.lbl_total.config(text=f"Tổng doanh thu (Demo): 150,000,000 VNĐ")