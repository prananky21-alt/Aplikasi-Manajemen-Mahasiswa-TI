import re
import json
import os
import hashlib
import getpass
from abc import ABC, abstractmethod

# ===== Fitur Login + Role =====
class Auth:
    def __init__(self, file_path='users.json'):
        self.file_path = file_path
        self.users = {}
        self.current_user = None
        self.load_users()
        # Bikin user admin default kalau belum ada
        if not self.users:
            self.register('admin', 'admin123', 'admin', 'apa nama dosen favoritmu?', 'pak budi')
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    self.users = json.load(f)
        except (IOError, json.JSONDecodeError):
            self.users = {}
    
    def save_users(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.users, f, indent=4)
        except IOError as e:
            print(f"Error simpan user: {e}")
    
    def register(self, username, password, role='user', pertanyaan=None, jawaban=None):
        if username in self.users:
            raise ValueError("Username sudah ada")
        if not re.match(r'^[a-zA-Z0-9]{3,20}$', username):
            raise ValueError("Username 3-20 karakter, huruf/angka aja")
        if len(password) < 6:
            raise ValueError("Password minimal 6 karakter")
        if role not in ['admin', 'user']:
            raise ValueError("Role harus admin atau user")
        
        self.users[username] = {
            'password': self.hash_password(password),
            'role': role,
            'pertanyaan': pertanyaan,
            'jawaban': self.hash_password(jawaban.lower()) if jawaban else None
        }
        self.save_users()
        return True
    
    def login(self, username, password):
        """Time Complexity: O(1) akses dict"""
        if username not in self.users:
            return False
        if self.users[username]['password'] == self.hash_password(password):
            self.current_user = username
            return True
        return False
    
    def get_role(self):
        if self.current_user:
            return self.users[self.current_user]['role']
        return None
    
    def logout(self):
        self.current_user = None
    
    def lupa_password(self, username):
        if username not in self.users:
            return False, "Username tidak ditemukan"
        
        user_data = self.users[username]
        if not user_data['pertanyaan']:
            return False, "User ini tidak set pertanyaan keamanan"
        
        print(f"Pertanyaan keamanan: {user_data['pertanyaan']}")
        jawaban = input("Jawaban kamu: ").lower()
        
        if self.hash_password(jawaban) == user_data['jawaban']:
            password_baru = getpass.getpass("Jawaban benar! Masukkan password baru: ")
            if len(password_baru) < 6:
                return False, "Password minimal 6 karakter"
            user_data['password'] = self.hash_password(password_baru)
            self.save_users()
            return True, "Password berhasil direset!"
        else:
            return False, "Jawaban salah!"

# ===== OOP: Base Class + Inheritance + Polymorphism =====
class Person(ABC):
    def __init__(self, nama, umur):
        self._nama = nama 
        self._umur = umur
    
    @abstractmethod
    def get_info(self):
        pass
    
    @property
    def nama(self):
        return self._nama
    
    @nama.setter
    def nama(self, value):
        if not re.match(r'^[A-Za-z\s]{3,50}$', value):
            raise ValueError("Nama hanya huruf & spasi, 3-50 karakter")
        self._nama = value

class Mahasiswa(Person):
    def __init__(self, nim, nama, umur, jurusan, ipk):
        super().__init__(nama, umur)
        self.nim = nim
        self.jurusan = jurusan
        self.ipk = ipk
    
    def get_info(self):
        return f"NIM: {self.nim} | {self._nama} | {self.jurusan} | IPK: {self.ipk}"
    
    def to_dict(self):
        return {
            'nim': self.nim, 'nama': self._nama, 
            'umur': self._umur, 'jurusan': self.jurusan, 'ipk': self.ipk
        }
    
    @staticmethod
    def from_dict(data):
        return Mahasiswa(data['nim'], data['nama'], data['umur'], 
                        data['jurusan'], data['ipk'])

# ===== Manajemen Data =====
class ManajemenMahasiswa:
    def __init__(self, file_path='data_mahasiswa.json'):
        self.data_mahasiswa = []
        self.file_path = file_path
        self.load_from_file()
    
    def save_to_file(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump([mhs.to_dict() for mhs in self.data_mahasiswa], f, indent=4)
        except IOError as e:
            print(f"Error simpan file: {e}")
    
    def load_from_file(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    self.data_mahasiswa = [Mahasiswa.from_dict(d) for d in data]
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error baca file: {e}. Mulai dengan data kosong.")
            self.data_mahasiswa = []

    def validasi_nim(self, nim):
        if not re.match(r'^\d{8,12}$', nim):
            raise ValueError("NIM harus 8-12 digit angka")
        if any(mhs.nim == nim for mhs in self.data_mahasiswa):
            raise ValueError("NIM sudah terdaftar")
        return True
    
    def validasi_ipk(self, ipk):
        if not re.match(r'^[0-4](\.\d{1,2})?$', str(ipk)):
            raise ValueError("IPK harus 0.00 - 4.00")
        return True

    def tambah_mahasiswa(self, mhs):
        try:
            self.validasi_nim(mhs.nim)
            self.validasi_ipk(mhs.ipk)
            self.data_mahasiswa.append(mhs)
            self.save_to_file()
            print("Mahasiswa berhasil ditambahkan")
        except ValueError as e:
            print(f"Error: {e}")
    
    def tampilkan_semua(self):
        if not self.data_mahasiswa:
            print("Data kosong")
            return
        print("\n=== DATA MAHASISWA ===")
        for idx, mhs in enumerate(self.data_mahasiswa, 1):
            print(f"{idx}. {mhs.get_info()}")
    
    def edit_mahasiswa(self, nim):
        for mhs in self.data_mahasiswa:
            if mhs.nim == nim:
                try:
                    nama_baru = input(f"Nama baru [{mhs.nama}]: ") or mhs.nama
                    mhs.nama = nama_baru
                    mhs.jurusan = input(f"Jurusan baru [{mhs.jurusan}]: ") or mhs.jurusan
                    ipk_baru = input(f"IPK baru [{mhs.ipk}]: ") or mhs.ipk
                    self.validasi_ipk(ipk_baru)
                    mhs.ipk = float(ipk_baru)
                    self.save_to_file()
                    print("Data berhasil diupdate")
                except ValueError as e:
                    print(f"Error: {e}")
                return
        print("NIM tidak ditemukan")
    
    def hapus_mahasiswa(self, nim):
        for i, mhs in enumerate(self.data_mahasiswa):
            if mhs.nim == nim:
                del self.data_mahasiswa[i]
                self.save_to_file()
                print("Data berhasil dihapus")
                return
        print("NIM tidak ditemukan")

    def linear_search(self, nim):
        for mhs in self.data_mahasiswa:
            if mhs.nim == nim:
                return mhs
        return None
    
    def bubble_sort_by_nim(self):
        n = len(self.data_mahasiswa)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.data_mahasiswa[j].nim > self.data_mahasiswa[j+1].nim:
                    self.data_mahasiswa[j], self.data_mahasiswa[j+1] = \
                        self.data_mahasiswa[j+1], self.data_mahasiswa[j]

# ===== Main Program + Login + Role =====
def menu_utama(app, auth):
    role = auth.get_role()
    
    while True:
        print(f"\n=== MENU MANAJEMEN MAHASISWA | Login sebagai: {auth.current_user} [{role}] ===")
        
        if role == 'admin':
            print("1. Tambah Data\n2. Tampilkan Semua\n3. Edit Data")
            print("4. Hapus Data\n5. Cari NIM\n6. Sort NIM\n0. Logout")
        else: # user biasa
            print("1. Tampilkan Semua\n2. Cari NIM\n3. Sort NIM\n0. Logout")
        
        try:
            pilihan = input("Pilih menu: ")
            
            if role == 'admin':
                if pilihan == '1':
                    nim = input("NIM: ")
                    nama = input("Nama: ")
                    umur = int(input("Umur: "))
                    jurusan = input("Jurusan: ")
                    ipk = float(input("IPK: "))
                    mhs = Mahasiswa(nim, nama, umur, jurusan, ipk)
                    app.tambah_mahasiswa(mhs)
                
                elif pilihan == '2':
                    app.tampilkan_semua()
                
                elif pilihan == '3':
                    nim = input("Masukkan NIM yang mau diedit: ")
                    app.edit_mahasiswa(nim)
                
                elif pilihan == '4':
                    nim = input("Masukkan NIM yang mau dihapus: ")
                    app.hapus_mahasiswa(nim)
                    
                elif pilihan == '5':
                    nim = input("Cari NIM: ")
                    hasil = app.linear_search(nim)
                    print(hasil.get_info() if hasil else "Tidak ditemukan")
                    
                elif pilihan == '6':
                    app.bubble_sort_by_nim()
                    print("Data berhasil diurutkan by NIM")
                    app.tampilkan_semua()
                    
                elif pilihan == '0':
                    auth.logout()
                    print("Logout berhasil!")
                    break
                else:
                    print("Pilihan tidak valid")
            
            else: # role user
                if pilihan == '1':
                    app.tampilkan_semua()
                elif pilihan == '2':
                    nim = input("Cari NIM: ")
                    hasil = app.linear_search(nim)
                    print(hasil.get_info() if hasil else "Tidak ditemukan")
                elif pilihan == '3':
                    app.bubble_sort_by_nim()
                    print("Data berhasil diurutkan by NIM")
                    app.tampilkan_semua()
                elif pilihan == '0':
                    auth.logout()
                    print("Logout berhasil!")
                    break
                else:
                    print("Pilihan tidak valid atau kamu bukan admin")
                
        except ValueError as e:
            print(f"Input error: {e}")
        except Exception as e:
            print(f"Terjadi error: {e}")

def main():
    auth = Auth()
    app = ManajemenMahasiswa()
    
    while True:
        print("\n=== APLIKASI MANAJEMEN MAHASISWA TI ===")
        print("1. Login\n2. Register\n3. Lupa Password\n0. Keluar")
        pilih = input("Pilih: ")
        
        if pilih == '1':
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            
            if auth.login(username, password):
                print(f"\nLogin berhasil! Selamat datang {username}")
                menu_utama(app, auth)
            else:
                print("Username atau password salah!")
        
        elif pilih == '2':
            try:
                username = input("Username baru: ")
                password = getpass.getpass("Password baru: ")
                role = input("Role [admin/user] default=user: ") or 'user'
                pertanyaan = input("Pertanyaan keamanan, contoh 'nama hewan peliharaan': ")
                jawaban = input("Jawaban: ")
                auth.register(username, password, role, pertanyaan, jawaban)
                print("Register berhasil! Silakan login")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif pilih == '3':
            username = input("Masukkan username kamu: ")
            sukses, pesan = auth.lupa_password(username)
            print(pesan)
        
        elif pilih == '0':
            print("Terima kasih!")
            break

if __name__ == "__main__":
    main()