import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aplikasi Manajemen Data Mahasiswa", layout="wide")

# --- 1. LOGIN SYSTEM ---
if 'login' not in st.session_state:
    st.session_state.login = False

def login_page():
    st.title("Login Aplikasi Manajemen Data Mahasiswa")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.login = True
            st.session_state.role = "admin"
            st.rerun()
        else:
            st.error("Username atau password salah!")

if not st.session_state.login:
    login_page()
    st.stop()

# --- 2. CSS TOMBOL WARNA-WARNI ---
st.markdown("""
<style>
.block-container {padding-top: 1rem;}
h2 {text-align: center; color: #1E3A8A; font-weight: 700;}
.stButton > button {
    border-radius: 4px; border: 1px solid #999;
    background-color: #EFEFEF; color: black;
}
.stButton > button[kind="primary"] {
    background-color: #4A90E2; color: white; border: none;
}
.stDataFrame {border: 1px solid #AAA;}

/* TOMBOL KANAN WARNA-WARNI */
.st-key-btn_tambah button {
    width: 100%; height: 70px; font-weight: bold; color: white!important;
    border: none!important; border-radius: 8px; margin-top: 10px; font-size: 16px;
    background-color: #4CAF50!important;
}
.st-key-btn_update button {
    width: 100%; height: 70px; font-weight: bold; color: white!important;
    border: none!important; border-radius: 8px; margin-top: 10px; font-size: 16px;
    background-color: #2196F3!important;
}
.st-key-btn_hapus button {
    width: 100%; height: 70px; font-weight: bold; color: white!important;
    border: none!important; border-radius: 8px; margin-top: 10px; font-size: 16px;
    background-color: #F44336!important;
}
.st-key-btn_bubble button {
    width: 100%; height: 70px; font-weight: bold; color: white!important;
    border: none!important; border-radius: 8px; margin-top: 10px; font-size: 16px;
    background-color: #9C27B0!important;
}
.st-key-btn_merge button {
    width: 100%; height: 70px; font-weight: bold; color: white!important;
    border: none!important; border-radius: 8px; margin-top: 10px; font-size: 16px;
    background-color: #FF9800!important;
}
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.write(f"Login sebagai: **{st.session_state.role}**")
    st.write(f"Role: {st.session_state.role}")
    if st.button("Logout"):
        st.session_state.login = False
        st.rerun()
    
    st.divider()
    st.subheader("Menu Admin")
    menu = st.selectbox("Pilih Menu", ["Tampilkan Semua", "Backup Data"], label_visibility="collapsed", index=0)
    
    st.divider()
    with st.expander("🔽 Backup Data"):
        df_backup = pd.DataFrame(st.session_state.get('data', []))
        st.download_button("Download JSON", df_backup.to_json(orient="records"), "data_mahasiswa.json", mime="application/json")

# --- 4. FUNGSI SORTING ---
def bubble_sort_nama(data):
    n = len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if data[j]['Nama'].lower() > data[j+1]['Nama'].lower():
                data[j], data[j+1] = data[j+1], data[j]
    return data

def merge_sort_nim(data):
    if len(data) > 1:
        mid = len(data)//2
        L = data[:mid]
        R = data[mid:]
        merge_sort_nim(L)
        merge_sort_nim(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i]['NIM'] < R[j]['NIM']:
                data[k] = L[i]
                i += 1
            else:
                data[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            data[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            data[k] = R[j]
            j += 1
            k += 1
    return data

# --- 5. DATA 10 MAHASISWA ---
if 'data' not in st.session_state:
    st.session_state.data = [
        {"NIM": "24010000", "Nama": "Firmansyah", "Umur": 20, "Jurusan": "Komputer", "IPK": 4.0},
        {"NIM": "24010006", "Nama": "Ega Ramadhany", "Umur": 19, "Jurusan": "Rekayasa Perangkat Lunak", "IPK": 3.95},
        {"NIM": "24010002", "Nama": "Novandi", "Umur": 19, "Jurusan": "Sistem Informasi", "IPK": 3.9},
        {"NIM": "24010004", "Nama": "Fahmi Maulana", "Umur": 20, "Jurusan": "Teknologi Informasi", "IPK": 3.85},
        {"NIM": "24010009", "Nama": "Glenadi", "Umur": 21, "Jurusan": "Teknik Komputer", "IPK": 3.8},
        {"NIM": "24010001", "Nama": "Pranan", "Umur": 21, "Jurusan": "Teknik Informatika", "IPK": 3.75},
        {"NIM": "24010008", "Nama": "Salwa Aulia", "Umur": 20, "Jurusan": "Sistem Informasi", "IPK": 3.7},
        {"NIM": "24010005", "Nama": "Eka Sri Rahayu", "Umur": 21, "Jurusan": "Ilmu Komputer", "IPK": 3.6},
        {"NIM": "24010003", "Nama": "Abdul Goni", "Umur": 22, "Jurusan": "Teknik Komputer", "IPK": 3.5},
        {"NIM": "24010007", "Nama": "Fadiyah", "Umur": 22, "Jurusan": "Teknik Informatika", "IPK": 3.4},
    ]
if 'data_filtered' not in st.session_state:
    st.session_state.data_filtered = st.session_state.data.copy()
if 'selected_idx' not in st.session_state:
    st.session_state.selected_idx = None
if 'show_dialog' not in st.session_state:
    st.session_state.show_dialog = False

# --- 6. HALAMAN UTAMA ---
if menu == "Tampilkan Semua":
    st.markdown("<h2>Data Mahasiswa</h2>", unsafe_allow_html=True)
    
    col_tabel, col_form = st.columns([3, 1.2])

    with col_tabel:
        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        with c1:
            cari = st.text_input("Cari Data:", placeholder="Cari Data:", label_visibility="collapsed")
        with c2:
            if st.button("Cari (Nama)", type="primary"):
                if cari:
                    st.session_state.data_filtered = [d for d in st.session_state.data if cari.lower() in d['Nama'].lower()]
                else:
                    st.session_state.data_filtered = st.session_state.data.copy()
        with c3:
            if st.button("Cari (NIM)"):
                if cari:
                    st.session_state.data_filtered = [d for d in st.session_state.data if cari in d['NIM']]
                else:
                    st.session_state.data_filtered = st.session_state.data.copy()
        with c4:
            if st.button("Reset Tabel"):
                st.session_state.data_filtered = st.session_state.data.copy()
                st.session_state.selected_idx = None

        df = pd.DataFrame(st.session_state.data_filtered)
        event = st.dataframe(df, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")
        
        if event.selection.rows:
            st.session_state.selected_idx = event.selection.rows[0]

    with col_form:
        selected_data = {"NIM": "", "Nama": "", "Umur": 17, "Jurusan": "", "IPK": 0.0}
        if st.session_state.selected_idx is not None and st.session_state.selected_idx < len(st.session_state.data_filtered):
            selected_data = st.session_state.data_filtered[st.session_state.selected_idx]

        nim = st.text_input("NIM (12 Digit Angka):", value=selected_data["NIM"])
        nama = st.text_input("Nama:", value=selected_data["Nama"])
        umur = st.number_input("Umur:", value=int(selected_data["Umur"]), min_value=17, max_value=60)
        jurusan = st.text_input("Jurusan:", value=selected_data["Jurusan"])
        ipk = st.number_input("IPK:", value=float(selected_data["IPK"]), min_value=0.0, max_value=4.0, step=0.01)

        if st.button("Tambah Data", key="btn_tambah"):
            if nim and nama and jurusan:
                if any(d['NIM'] == nim for d in st.session_state.data):
                    st.error("NIM sudah ada!")
                else:
                    st.session_state.data.append({"NIM": nim, "Nama": nama, "Umur": umur, "Jurusan": jurusan, "IPK": ipk})
                    st.session_state.data_filtered = st.session_state.data.copy()
                    st.success("Data berhasil ditambah!")
                    st.rerun()
            else:
                st.error("NIM, Nama, Jurusan harus diisi!")

        if st.button("Update Data", key="btn_update"):
            if st.session_state.selected_idx is not None:
                nim_lama = st.session_state.data_filtered[st.session_state.selected_idx]['NIM']
                for i, d in enumerate(st.session_state.data):
                    if d['NIM'] == nim_lama:
                        st.session_state.data[i] = {"NIM": nim, "Nama": nama, "Umur": umur, "Jurusan": jurusan, "IPK": ipk}
                        break
                st.session_state.data_filtered = st.session_state.data.copy()
                st.success("Data berhasil diupdate!")
                st.rerun()
            else:
                st.warning("Pilih data di tabel dulu!")

        if st.button("Hapus Data", key="btn_hapus"):
            if st.session_state.selected_idx is not None:
                st.session_state.show_dialog = True
                st.rerun()
            else:
                st.warning("Pilih data dulu!")

        if st.button("Urutkan (Nama - Bubble)", key="btn_bubble"):
            st.session_state.data_filtered = bubble_sort_nama(st.session_state.data_filtered.copy())
            st.toast("Data diurutkan Nama - Bubble Sort")
            st.rerun()

        if st.button("Urutkan (NIM - Merge)", key="btn_merge"):
            st.session_state.data_filtered = merge_sort_nim(st.session_state.data_filtered.copy())
            st.toast("Data diurutkan NIM - Merge Sort")
            st.rerun()

elif menu == "Backup Data":
    st.subheader("Backup Data")
    st.dataframe(pd.DataFrame(st.session_state.data), use_container_width=True, hide_index=True)

# --- 7. DIALOG HAPUS ---
if st.session_state.show_dialog:
    @st.dialog("Konfirmasi")
    def hapus_dialog():
        nim_hapus = st.session_state.data_filtered[st.session_state.selected_idx]['NIM']
        st.write(f"Yakin hapus NIM: {nim_hapus}?")
        col1, col2 = st.columns(2)
        if col1.button("Yes", type="primary"):
            st.session_state.data = [d for d in st.session_state.data if d['NIM']!= nim_hapus]
            st.session_state.data_filtered = st.session_state.data.copy()
            st.session_state.show_dialog = False
            st.session_state.selected_idx = None
            st.rerun()
        if col2.button("No"):
            st.session_state.show_dialog = False
            st.rerun()
    hapus_dialog()
