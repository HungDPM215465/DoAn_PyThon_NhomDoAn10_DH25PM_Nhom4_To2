import pyodbc
import hashlib
from tkinter import messagebox


SERVER = '.\QUOCHUNG'      
DATABASE = 'quanly_tivi'
DRIVER = 'SQL Server'      


CONNECTION_STRING = f"""
    DRIVER={{{DRIVER}}};
    SERVER={SERVER};
    DATABASE={DATABASE};
    Trusted_Connection=yes;
"""

def create_connection():
    """Tạo và trả về một đối tượng kết nối CSDL"""
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '28000':
            messagebox.showerror("Lỗi kết nối", "Lỗi xác thực. Kiểm tra lại Username/Password hoặc Trusted_Connection.")
        elif sqlstate == '08001':
            messagebox.showerror("Lỗi kết nối", "Không tìm thấy Server hoặc Driver. Kiểm tra lại tên Server và Driver.")
        elif sqlstate == '42000':
             messagebox.showerror("Lỗi kết nối", f"Không tìm thấy Database '{DATABASE}'.")
        else:
            messagebox.showerror("Lỗi kết nối", f"Lỗi: {ex}")
        return None
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi không xác định: {e}")
        return None

def fetch_all(query, params=None):
    """Chạy lệnh SELECT và trả về TẤT CẢ các hàng (dưới dạng list of dicts)"""
    conn = create_connection()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
       
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
            
        return results
        
    except pyodbc.Error as e:
        messagebox.showerror("Lỗi truy vấn", f"Lỗi fetch: {e}")
        return []
    finally:
        if conn:
            conn.close()

def execute_query(query, params=None):
    """Chạy lệnh (INSERT, UPDATE, DELETE) và trả về True/False"""
    conn = create_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return True
    except pyodbc.Error as e:
        conn.rollback() 
        messagebox.showerror("Lỗi truy vấn", f"Lỗi execute: {e}")
        return False
    finally:
        if conn:
            conn.close()

def lay_danh_sach_tivi():
    
    return fetch_all("SELECT id_tv, ten_tv, hang_san_xuat, model, gia_ban, so_luong_ton FROM tivi")

def them_tivi(ten_tv, hang_sx, model, gia_ban, so_luong):
    """Thêm một TV mới vào CSDL"""
    query = """
    INSERT INTO tivi (ten_tv, hang_san_xuat, model, gia_ban, so_luong_ton)
    VALUES (?, ?, ?, ?, ?)
    """

    params = (ten_tv, hang_sx, model, gia_ban, so_luong)
    return execute_query(query, params)

def sua_tivi(id_tv, ten_tv, hang_sx, model, gia_ban, so_luong):
    """Cập nhật thông tin một TV dựa vào ID"""
    query = """
    UPDATE tivi
    SET ten_tv = ?, hang_san_xuat = ?, model = ?, gia_ban = ?, so_luong_ton = ?
    WHERE id_tv = ?
    """
    params = (ten_tv, hang_sx, model, gia_ban, so_luong, id_tv)
    return execute_query(query, params)

def xoa_tivi(id_tv):
    """Xóa một TV khỏi CSDL dựa vào ID"""
    query = "DELETE FROM tivi WHERE id_tv = ?"
    params = (id_tv,)
    return execute_query(query, params)



def lay_danh_sach_khach_hang():
    """Lấy toàn bộ Khách Hàng từ CSDL"""
    query = "SELECT id_kh, ten_kh, so_dien_thoai, dia_chi, email FROM khach_hang"
    return fetch_all(query)

def them_khach_hang(ten, sdt, dia_chi, email):
    """Thêm khách hàng mới"""
    query = """
    INSERT INTO khach_hang (ten_kh, so_dien_thoai, dia_chi, email)
    VALUES (?, ?, ?, ?)
    """
    params = (ten, sdt, dia_chi, email)
    return execute_query(query, params)

def sua_khach_hang(id_kh, ten, sdt, dia_chi, email):
    """Sửa thông tin khách hàng"""
    query = """
    UPDATE khach_hang
    SET ten_kh = ?, so_dien_thoai = ?, dia_chi = ?, email = ?
    WHERE id_kh = ?
    """
    params = (ten, sdt, dia_chi, email, id_kh)
    return execute_query(query, params)

def xoa_khach_hang(id_kh):
    """Xóa khách hàng"""
    query = "DELETE FROM khach_hang WHERE id_kh = ?"
    params = (id_kh,)
    return execute_query(query, params)


def lay_danh_sach_ncc():
    return fetch_all("SELECT * FROM nha_cung_cap")

def them_ncc(ten, dia_chi, sdt, email):
    query = "INSERT INTO nha_cung_cap (ten_ncc, dia_chi, so_dien_thoai, email) VALUES (?, ?, ?, ?)"
    return execute_query(query, (ten, dia_chi, sdt, email))

def sua_ncc(id_ncc, ten, dia_chi, sdt, email):
    query = "UPDATE nha_cung_cap SET ten_ncc=?, dia_chi=?, so_dien_thoai=?, email=? WHERE id_ncc=?"
    return execute_query(query, (ten, dia_chi, sdt, email, id_ncc))

def xoa_ncc(id_ncc):
    return execute_query("DELETE FROM nha_cung_cap WHERE id_ncc=?", (id_ncc,))


def lay_danh_sach_nv():

    return fetch_all("SELECT id_nv, ma_nv, ho_lot, ten, gioi_tinh, ngay_sinh, chuc_vu FROM nhan_vien")

def them_nv(ho, ten, phai, ngay_sinh, chuc_vu):
    query = "INSERT INTO nhan_vien (ho_lot, ten, gioi_tinh, ngay_sinh, chuc_vu) VALUES (?, ?, ?, ?, ?)"
    return execute_query(query, (ho, ten, phai, ngay_sinh, chuc_vu))

def sua_nv(id_nv, ho, ten, phai, ngay_sinh, chuc_vu):
    query = "UPDATE nhan_vien SET ho_lot=?, ten=?, gioi_tinh=?, ngay_sinh=?, chuc_vu=? WHERE id_nv=?"
    return execute_query(query, (ho, ten, phai, ngay_sinh, chuc_vu, id_nv))

def xoa_nv(id_nv):
    return execute_query("DELETE FROM nhan_vien WHERE id_nv=?", (id_nv,))


def lay_danh_sach_hoa_don():
    query = """
    SELECT hd.id_hd, kh.ten_kh, hd.ngay_lap, hd.tong_tien, hd.trang_thai
    FROM hoa_don hd
    JOIN khach_hang kh ON hd.id_kh = kh.id_kh
    ORDER BY hd.ngay_lap DESC
    """
    return fetch_all(query)

def lay_chi_tiet_hoa_don(id_hd):
    query = """
    SELECT tv.ten_tv, cthd.so_luong, cthd.don_gia_luc_ban, (cthd.so_luong * cthd.don_gia_luc_ban) as thanh_tien
    FROM chi_tiet_hoa_don cthd
    JOIN tivi tv ON cthd.id_tv = tv.id_tv
    WHERE cthd.id_hd = ?
    """
    return fetch_all(query, (id_hd,))

def tao_hoa_don_moi(id_kh, gio_hang):
    conn = create_connection()
    if conn is None: return False
    cursor = conn.cursor()
    try:
        tong_tien = sum(item['so_luong'] * item['don_gia'] for item in gio_hang)
        
        cursor.execute("INSERT INTO hoa_don (id_kh, tong_tien, trang_thai) VALUES (?, ?, ?)", (id_kh, tong_tien, 'Hoàn thành'))
        cursor.execute("SELECT @@IDENTITY")
        id_hd = cursor.fetchone()[0]

        for item in gio_hang:
            cursor.execute("INSERT INTO chi_tiet_hoa_don (id_hd, id_tv, so_luong, don_gia_luc_ban) VALUES (?, ?, ?, ?)", 
                           (id_hd, item['id_tv'], item['so_luong'], item['don_gia']))
            cursor.execute("UPDATE tivi SET so_luong_ton = so_luong_ton - ? WHERE id_tv = ?", 
                           (item['so_luong'], item['id_tv']))

        conn.commit()
        return True
    except Exception as e:
        print("Lỗi:", e)
        conn.rollback()
        return False
    finally:
        conn.close()

def ma_hoa_mat_khau(password):
    """Mã hóa mật khẩu sang chuỗi SHA256 để bảo mật"""
    return hashlib.sha256(password.encode()).hexdigest()

def kiem_tra_dang_nhap(username, password):
    """Kiểm tra user/pass. Trả về True nếu đúng, False nếu sai"""
    conn = create_connection()
    if not conn: return False
 
    pass_hash = ma_hoa_mat_khau(password)
    
    cursor = conn.cursor()
    query = "SELECT * FROM tai_khoan WHERE ten_dang_nhap = ? AND mat_khau = ?"
    cursor.execute(query, (username, pass_hash))
    
    user = cursor.fetchone()
    conn.close()
    
    return True if user else False

def dang_ky_tai_khoan(username, password, fullname, email):
    """Tạo tài khoản mới"""
    conn = create_connection()
    if not conn: return False
    
    try:
        pass_hash = ma_hoa_mat_khau(password)
        cursor = conn.cursor()
        query = "INSERT INTO tai_khoan (ten_dang_nhap, mat_khau, ho_ten, email) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (username, pass_hash, fullname, email))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Lỗi đăng ký:", e)
        return False

def kiem_tra_dang_nhap(username, password):
    """
    Kiểm tra user/pass. 
    Trả về 'role' (admin/customer) nếu đúng.
    Trả về None nếu sai.
    """
    conn = create_connection()
    if not conn: return None
    
    pass_hash = ma_hoa_mat_khau(password)
    
    cursor = conn.cursor()
    
    query = "SELECT vai_tro FROM tai_khoan WHERE ten_dang_nhap = ? AND mat_khau = ?"
    cursor.execute(query, (username, pass_hash))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return row[0] 
    else:
        return None