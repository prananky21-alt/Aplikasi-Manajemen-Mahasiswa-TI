import re
import json
import os
import hashlib
import streamlit as st
import pandas as pd
from abc import ABC, abstractmethod

st.set_page_config(page_title="Manajemen Mahasiswa TI", layout="wide")

# ===== Fitur Login + Role =====
class Auth:
    def __init__(self, file_path='users.json'):
        self.file_path = file_path
        self.users = {}
        self.load_users()
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
            st.error(f"Error simpan user: {e}")

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
        if username not in self.users:
            return False
        if self.users[username]['password'] == self.hash_password(password):
            st.session_state.current_user = username
            st.session_state.role = self.users[username]['role']
            return True
        return False

    def get_role(self):
        return st.session_state.get('role', None)

    def logout(self):
        st.session_state.current_user = None
        st.session_state.role = None

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
            st.error(f"Error simpan file: {e}")

    def load_from_file(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    self.data_mahasiswa = [Mahasiswa.from_dict(d) for d in data]
        except (IOError, json.JSONDecodeError) as e:
            st.warning(f"Error baca file: {e}. Mulai dengan data kosong.")
            self.data_mahasiswa = []

    def validasi_nim(self, nim):
        if not re.match(r'^\d{8,12}$', nim):
            raise ValueError("NIM harus 8-12 digit angka")
        if any(mhs.nim == nim for mhs in self.data_mahasiswa):
            raise ValueError("NIM sudah terdaftar")
        return True

    def validasi_ipk(self, ipk):
        if not (0.0 <= float(ipk) <= 4.0):
            raise ValueError("IPK harus 0.00 - 4.00")
        return True

    def tambah_mahasiswa(self, mhs):
        self.validasi_nim(mhs.nim)
        self.validasi_ipk(mhs.ipk)
        self.data_mahasiswa.append(mhs)
        self.save_to_file()
        st.success("Mahasiswa berhasil ditambahkan")

    def get_dataframe(self):
        if not self.data_mahasiswa:
            return pd.DataFrame()
        return pd.DataFrame([m.to_dict() for m in self.data_mahasiswa])

    def edit_mahasiswa(self, nim, nama_baru, jurusan_baru, ipk_baru):
        for mhs in self.data_mahasiswa:
            if mhs.nim == nim:
                mhs.nama = nama_baru
                mhs.jurusan = jurusan_baru
                self.validasi_ipk(ipk_baru)
                mhs.ipk = float(ipk_baru)
                self.save_to_file()
                st.success("Data berhasil diupdate")
                return True
        st.error("NIM tidak ditemukan")
        return False

    def hapus_mahasiswa(self, nim):
        for i, mhs in enumerate(self.data_mahasiswa):
            if mhs.nim == nim:
                del self.data_mahasiswa[i]
                self.save_to_file()
                st.success("Data berhasil dihapus")
                return True
        st.error("NIM tidak ditemukan")
        return False

    def linear_search(self, nim):
        """Linear Search by NIM. Time Complexity: O(n)"""
        for mhs in self.data_mahasiswa:
            if mhs.nim == nim:
                return mhs
        return None

    def bubble_sort_by_nim(self):
        """Bubble Sort by NIM ascending. Time Complexity: O(n²)"""
        n = len(self.data_mahasiswa)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.data_mahasiswa[j].nim > self.data_mahasiswa[j+1].nim:
                    self.data_mahasiswa[j], self.data_mahasiswa[j+1] = \
                        self.data_mahasiswa[j+1], self.data_mahasiswa[j]
        self.save_to_file()

    def selection_sort_by_ipk(self):
        """Selection Sort by IPK descending. Time Complexity: O(n²)"""
        n = len(self.data_mahasiswa)
        for i in range(n):
            max_idx = i
            for j in range(i+1, n):
                if self.data_mahasiswa[j].ipk > self.data_mahasiswa[max_idx].ipk:
                    max_idx = j
            self.data_mahasiswa[i], self.data_mahasiswa[max_idx] = \
                self.data_mahasiswa[max_idx], self.data_mahasiswa[i]
        self.save_to_file()

# ===== Streamlit UI =====
def init_session():
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'role' not in st.session_state:
        st.session_state.role = None

def login_page(auth):
    st.title("APLIKASI MANAJEMEN MAHASISWA TI")
    tab1, tab2, tab3 = st.tabs(["Login", "Register", "Lupa Password"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if auth.login(username, password):
                st.success(f"Login berhasil! Selamat datang {username}")
                st.rerun()
            else:
                st.error("Username atau password salah!")

    with tab2:
        st.subheader("Register")
        new_user = st.text_input("Username baru", key="reg_user")
        new_pass = st.text_input("Password baru", type="password", key="reg_pass")
        role = st.selectbox("Role", ["user", "admin"], key="reg_role")
        pertanyaan = st.text_input("Pertanyaan keamanan", key="reg_q")
        jawaban = st.text_input("Jawaban", key="reg_a")
        if st.button("Register"):
            try:
                auth.register(new_user, new_pass, role, pertanyaan, jawaban)
                st.success("Register berhasil! Silakan login")
            except ValueError as e:
                st.error(f"Error: {e}")

    with tab3:
        st.subheader("Lupa Password")
        username_lp = st.text_input("Masukkan username kamu", key="lp_user")
        if username_lp and username_lp in auth.users:
            st.info(f"Pertanyaan: {auth.users[username_lp]['pertanyaan']}")
            jawaban_lp = st.text_input("Jawaban kamu", key="lp_ans")
            pass_baru = st.text_input("Password baru", type="password", key="lp_pass")
            if st.button("Reset Password"):
                if auth.hash_password(jawaban_lp.lower()) == auth.users[username_lp]['jawaban']:
                    if len(pass_baru) < 6:
                        st.error("Password minimal 6 karakter")
                    else:
                        auth.users[username_lp]['password'] = auth.hash_password(pass_baru)
                        auth.save_users()
                        st.success("Password berhasil direset!")
                else:
                    st.error("Jawaban salah!")

def main_app(auth, app):
    st.sidebar.title(f"Login sebagai: {st.session_state.current_user}")
    st.sidebar.markdown(f"**Role: {st.session_state.role}**")
    if st.sidebar.button("Logout"):
        auth.logout()
        st.rerun()

    role = st.session_state.role
    st.title("Dashboard Manajemen Mahasiswa")

    if role == 'admin':
        menu = st.sidebar.selectbox("Menu Admin", [
            "Tampilkan Semua", "Tambah Data", "Edit Data",
            "Hapus Data", "Cari NIM", "Sort Data"
        ])
    else:
        menu = st.sidebar.selectbox("Menu User", [
            "Tampilkan Semua", "Cari NIM", "Sort Data"
        ])

    if menu == "Tampilkan Semua":
        st.subheader("Data Mahasiswa")
        df = app.get_dataframe()
        if df.empty:
            st.warning("Data kosong")
        else:
            st.dataframe(df, use_container_width=True)

    elif menu == "Tambah Data" and role == 'admin':
        st.subheader("Tambah Mahasiswa")
        with st.form("tambah_form"):
            nim = st.text_input("NIM")
            nama = st.text_input("Nama")
            umur = st.number_input("Umur", min_value=15, max_value=60, value=20)
            jurusan = st.text_input("Jurusan")
            ipk = st.number_input("IPK", min_value=0.0, max_value=4.0, value=2.0, step=0.01)
            submitted = st.form_submit_button("Tambah")
            if submitted:
                try:
                    mhs = Mahasiswa(nim, nama, umur, jurusan, ipk)
                    app.tambah_mahasiswa(mhs)
                    st.rerun()
                except ValueError as e:
                    st.error(f"Error: {e}")

    elif menu == "Edit Data" and role == 'admin':
        st.subheader("Edit Mahasiswa")
        nim_edit = st.text_input("Masukkan NIM yang mau diedit")
        mhs = app.linear_search(nim_edit) if nim_edit else None
        if mhs:
            with st.form("edit_form"):
                nama_baru = st.text_input("Nama", value=mhs.nama)
                jurusan_baru = st.text_input("Jurusan", value=mhs.jurusan)
                ipk_baru = st.number_input("IPK", value=float(mhs.ipk), min_value=0.0, max_value=4.0, step=0.01)
                submitted = st.form_submit_button("Update")
                if submitted:
                    try:
                        app.edit_mahasiswa(nim_edit, nama_baru, jurusan_baru, ipk_baru)
                        st.rerun()
                    except ValueError as e:
                        st.error(f"Error: {e}")
        elif nim_edit:
            st.warning("NIM tidak ditemukan")

    elif menu == "Hapus Data" and role == 'admin':
        st.subheader("Hapus Mahasiswa")
        nim_hapus = st.text_input("Masukkan NIM yang mau dihapus")
        if st.button("Hapus", type="primary"):
            app.hapus_mahasiswa(nim_hapus)
            st.rerun()

    elif menu == "Cari NIM":
        st.subheader("Cari Mahasiswa by NIM - Linear Search O(n)")
        nim_cari = st.text_input("Masukkan NIM")
        if st.button("Cari"):
            hasil = app.linear_search(nim_cari)
            if hasil:
                st.success("Data ditemukan:")
                st.json(hasil.to_dict())
            else:
                st.warning("Tidak ditemukan")

    elif menu == "Sort Data":
        st.subheader("Urutkan Data")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sort by NIM - Bubble Sort"):
                app.bubble_sort_by_nim()
                st.success("Data diurutkan by NIM - Bubble Sort O(n²)")
                st.rerun()
        with col2:
            if st.button("Sort by IPK - Selection Sort"):
                app.selection_sort_by_ipk()
                st.success("Data diurutkan by IPK - Selection Sort O(n²)")
                st.rerun()
        st.dataframe(app.get_dataframe(), use_container_width=True)

    # === Tambahan: Backup & Download Data ===
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔽 Backup Data")

    if st.sidebar.button("Download JSON"):
        try:
            with open("data_mahasiswa.json", "r") as f:
                data_json = json.load(f)

            st.sidebar.download_button(
                label="⬇ Download data_mahasiswa.json",
                data=json.dumps(data_json, indent=2, ensure_ascii=False),
                file_name="data_mahasiswa.json",
                mime="application/json"
            )
            st.subheader("Isi data_mahasiswa.json")
            st.json(data_json)
        except Exception as e:
            st.sidebar.error(f"Error: {e}")
    # === End Tambahan ===

def main():
    init_session()
    auth = Auth()
    app = ManajemenMahasiswa()

    if st.session_state.current_user is None:
        login_page(auth)
    else:
        main_app(auth, app)

if __name__ == "__main__":
    main()
