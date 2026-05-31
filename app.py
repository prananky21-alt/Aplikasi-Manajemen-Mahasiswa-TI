import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aplikasi Manajemen Data Mahasiswa", layout="wide")

# --- 1. CSS Biar Mirip Swing ---
st.markdown("""
<style>
    /* Hilangin padding bawaan streamlit */
   .block-container {
        padding-top: 2rem;
    }
    
    /* Judul tengah kayak Swing */
    h2 {
        text-align: center;
        color: #1E3A8A;
        font-weight: 700;
    }

    /* Tombol Cari, Reset */
   .stButton > button {
        border-radius: 4px;
        border: 1px solid #999;
        background-color: #EFEFEF;
        color: black;
    }
   .stButton > button[kind="primary"] {
        background-color: #4A90E2;
        color: white;
        border: none;
    }

    /* Tombol kanan warna-warni */
    div[data-testid="column"]:nth-of-type(2).stButton > button {
        width: 100%;
        height: 70px;
        font-weight: bold;
        color: white;
        border: none;
        border-radius: 8px;
        margin-top: 10px;
        font-size: 16px;
    }
    #btn-tambah button { background-color: #4CAF50; }
    #btn-update button { background-color: #2196F3; }
    #btn-hapus button { background-color: #F44336; }
    #btn-bubble button { background-color: #9C27B0; }
    #btn-merge button { background-color: #FF9800; }
    
    /* Biar dataframe ada border kayak JTable */
   .stDataFrame {
        border: 1px solid #AAA;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. Inisialisasi Data ---
if 'data' not in st.session_state:
    st.session_state.data = [
        {"NIM": "221011400822", "Nama": "Sahrul Ramadhani", "Jurusan": "Teknik Informatika"},
        {"NIM": "221011400823", "Nama": "Arni Susanti Ndruru", "Jurusan": "Teknik Informatika"},
    ]
if 'selected_nim' not in st.session_state:
    st.session_state.selected_nim = None
if 'show_dialog' not in st.session_state:
    st.session_state.show_dialog = False

# --- 3. Judul ---
st.markdown("<h2>Data Mahasiswa</h2>", unsafe_allow_html=True)
st.write("")

# --- 4. Layout 2 Kolom: Tabel | Form ---
col_tabel, col_form = st.columns([3, 1.2])

with col_tabel:
    # Bar Cari Data
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1:
        cari = st.text_input("Cari Data:", placeholder="Cari Data:", label_visibility="collapsed")
    with c2:
        if st.button("Cari (Nama)", type="primary"):
            st.toast(f"Cari nama: {cari}")
    with c3:
        if st.button("Cari (NIM)"):
            st.toast(f"Cari NIM: {cari}")
    with c4:
        if st.button("Reset Tabel"):
            st.toast("Tabel direset")

    # Tabel Data
    df = pd.DataFrame(st.session_state.data)
    event = st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row"
    )
    
    # Kalo ada baris diklik, update form kanan
    if event.selection.rows:
        selected_idx = event.selection.rows[0]
        st.session_state.selected_nim = df.iloc[selected_idx]["NIM"]
        st.session_state.selected_nama = df.iloc[selected_idx]["Nama"]
        st.session_state.selected_jurusan = df.iloc[selected_idx]["Jurusan"]

with col_form:
    st.text_input("NIM (12 Digit Angka):", key="input_nim", value=st.session_state.get('selected_nim', ''))
    st.text_input("Nama:", key="input_nama", value=st.session_state.get('selected_nama', ''))
    st.text_input("Jurusan:", key="input_jurusan", value=st.session_state.get('selected_jurusan', ''))

    st.markdown('<div id="btn-tambah">', unsafe_allow_html=True)
    if st.button("Tambah Data"):
        st.session_state.data.append({
            "NIM": st.session_state.input_nim,
            "Nama": st.session_state.input_nama,
            "Jurusan": st.session_state.input_jurusan
        })
        st.toast("Data ditambah!")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div id="btn-update">', unsafe_allow_html=True)
    if st.button("Update Data"):
        st.toast("Data diupdate!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div id="btn-hapus">', unsafe_allow_html=True)
    if st.button("Hapus Data"):
        if st.session_state.get('selected_nim'):
            st.session_state.show_dialog = True
            st.rerun()
        else:
            st.warning("Pilih data dulu!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div id="btn-bubble">', unsafe_allow_html=True)
    if st.button("Urutkan (Nama - Bubble)"):
        st.toast("Urut Bubble Sort")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div id="btn-merge">', unsafe_allow_html=True)
    if st.button("Urutkan (NIM - Merge)"):
        st.toast("Urut Merge Sort")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. Dialog Konfirmasi Hapus ---
if st.session_state.show_dialog:
    @st.dialog("Konfirmasi")
    def hapus_dialog():
        st.write(f"Yakin hapus NIM: {st.session_state.selected_nim}?")
        col1, col2 = st.columns(2)
        if col1.button("Yes", type="primary"):
            st.session_state.data = [d for d in st.session_state.data if d["NIM"]!= st.session_state.selected_nim]
            st.session_state.show_dialog = False
            st.session_state.selected_nim = None
            st.rerun()
        if col2.button("No"):
            st.session_state.show_dialog = False
            st.rerun()
    hapus_dialog()
