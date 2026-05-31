import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aplikasi Manajemen Data Mahasiswa", layout="wide")

# --- 1. CSS Biar Mirip Swing + Tombol Warna ---
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
    /* Target tombol kanan pake key */
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"].stButton > button {
        width: 100%; height: 70px; font-weight: bold; color: white;
        border: none; border-radius: 8px; margin-top: 10px; font-size: 16px;
    }
    div[key="btn_tambah"] button { background-color: #4CAF50!important; }
    div[key="btn_update"] button { background-color: #2196F3!important; }
    div[key="btn_hapus"] button { background-color: #F44336!important; }
    div[key="btn_bubble"] button { background-color: #9C27B0!important; }
    div[key="btn_merge"] button { background-color: #FF9800!important; }
 .stDataFrame {border: 1px solid #AAA;}
</style>
""", unsafe_allow_html=True)

# --- 2. Fungsi Sorting ---
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
                data[k] = L[i]; i += 1
            else:
                data[k] = R[j]; j += 1
            k += 1
        while i < len(L): data[k] = L[i]; i+=1; k+=1
        while j < len(R): data[k] = R[j]; j+=1; k+=1
    return data

# --- 3. Inisialisasi Session State ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'users' not in st.session_state:
    st.session_state.users = {"admin": "admin123"} # username: password
if 'data' not in st.session_state:
    st.session_state.data = [
        {"NIM": "221011400822", "Nama": "Sahrul Ramadhani", "Jurusan": "Teknik Informatika"},
        {"NIM": "221011400823", "Nama": "Arni Susanti Ndruru", "Jurusan": "Teknik Informatika"},
        {"NIM": "24010001", "Nama": "Budi Santoso", "Jurusan": "Teknik Informatika"},
        {"NIM": "24010002", "Nama": "Siti Nurhaliza", "Jurusan": "Sistem Informasi"},
        {"NIM": "24010003", "Nama": "Ahmad Rizki", "Jurusan": "Teknik Komputer"},
        {"NIM": "24010004", "Nama": "Dewi Lestari", "Jurusan": "Teknologi Informasi"},
        {"NIM": "24010005", "Nama": "Rudi Hartono", "Jurusan": "Ilmu Komputer"},
        {"NIM": "24010006", "Nama": "Maya Sari", "Jurusan": "Rekayasa Perangkat Lunak"},
        {"NIM": "24010007", "Nama": "Joko Susanto", "Jurusan": "Teknik Informatika"},
        {"NIM": "24010008", "Nama": "Ani Wijaya", "Jurusan": "Sistem Informasi"},
    ]
if 'data_filtered' not in st.session_state:
    st.session_state.data_filtered = st.session_state.data.copy()
if 'selected_idx' not in st.session_state:
    st.session_state.selected_idx = None
if 'show_dialog' not in st.session_state:
    st.session_state.show_dialog = False

# --- 4. Halaman Login/Register ---
def login_page():
    st.title("Login Aplikasi Manajemen Data Mahasiswa")
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Username atau password salah")
    
    with tab2:
        new_user = st.text_input("Username Baru")
        new_pass = st.text_input("Password Baru", type="password")
        if st.button("Register"):
            if new_user in st.session_state.users:
                st.error("Username sudah ada")
            elif new_user and new_pass:
                st.session_state.users[new_user] = new_pass
                st.success("Register berhasil! Silakan login")
            else:
                st.error("Isi semua field")

# --- 5. Halaman Utama Setelah Login ---
def main_page():
    # Sidebar buat logout
    with st.sidebar:
        st.write(f"Login sebagai: **{st.session_state.username}**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        
        st.divider()
        st.write("**Backup Data**")
        df_download = pd.DataFrame(st.session_state.data)
        st.download_button("Download JSON", df_download.to_json(orient="records"), "data.json")

    st.markdown("<h2>Data Mahasiswa</h2>", unsafe_allow_html=True)
    st.write("")

    col_tabel, col_form = st.columns([3, 1.2])

    with col_tabel:
        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        with c1:
            cari = st.text_input("Cari Data:", placeholder="Cari Data:", label_visibility="collapsed")
        with c2:
            if st.button("Cari (Nama)", type="primary"):
                st.session_state.data_filtered = [d for d in st.session_state.data if cari.lower() in d['Nama'].lower()] if cari else st.session_state.data.copy()
        with c3:
            if st.button("Cari (NIM)"):
                st.session_state.data_filtered = [d for d in st.session_state.data if cari in d['NIM']] if cari else st.session_state.data.copy()
        with c4:
            if st.button("Reset Tabel"):
                st.session_state.data_filtered = st.session_state.data.copy()
                st.session_state.selected_idx = None

        df = pd.DataFrame(st.session_state.data_filtered)
        event = st.dataframe(df, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")
        
        if event.selection.rows:
            st.session_state.selected_idx = event.selection.rows[0]

    with col_form:
        selected_data = {"NIM": "", "Nama": "", "Jurusan": ""}
        if st.session_state.selected_idx is not None and st.session_state.selected_idx < len(st.session_state.data_filtered):
            selected_data = st.session_state.data_filtered[st.session_state.selected_idx]

        nim = st.text_input("NIM (12 Digit Angka):", value=selected_data["NIM"])
        nama = st.text_input("Nama:", value=selected_data["Nama"])
        jurusan = st.text_input("Jurusan:", value=selected_data["Jurusan"])

        if st.button("Tambah Data", key="btn_tambah"):
            if nim and nama and jurusan:
                if any(d['NIM'] == nim for d in st.session_state.data):
                    st.error("NIM sudah ada!")
                else:
                    st.session_state.data.append({"NIM": nim, "Nama": nama, "Jurusan": jurusan})
                    st.session_state.data_filtered = st.session_state.data.copy()
                    st.success("Data ditambah!")
                    st.rerun()
            else: st.error("Semua field harus diisi!")

        if st.button("Update Data", key="btn_update"):
            if st.session_state.selected_idx is not None:
                nim_lama = st.session_state.data_filtered[st.session_state.selected_idx]['NIM']
                for i, d in enumerate(st.session_state.data):
                    if d['NIM'] == nim_lama:
                        st.session_state.data[i] = {"NIM": nim, "Nama": nama, "Jurusan": jurusan}
                        break
                st.session_state.data_filtered = st.session_state.data.copy()
                st.success("Data diupdate!")
                st.rerun()
            else: st.warning("Pilih data di tabel dulu!")

        if st.button("Hapus Data", key="btn_hapus"):
            if st.session_state.selected_idx is not None:
                st.session_state.show_dialog = True
                st.rerun()
            else: st.warning("Pilih data dulu!")

        if st.button("Urutkan (Nama - Bubble)", key="btn_bubble"):
            st.session_state.data_filtered = bubble_sort_nama(st.session_state.data_filtered.copy())
            st.toast("Data diurutkan Nama - Bubble Sort")
            st.rerun()

        if st.button("Urutkan (NIM - Merge)", key="btn_merge"):
            st.session_state.data_filtered = merge_sort_nim(st.session_state.data_filtered.copy())
            st.toast("Data diurutkan NIM - Merge Sort")
            st.rerun()

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

# --- 6. Router ---
if st.session_state.logged_in:
    main_page()
else:
    login_page()
