import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aplikasi Manajemen Data Mahasiswa", layout="wide")

# --- 1. LOGIN SYSTEM ---
if 'login' not in st.session_state:
    st.session_state.login = False

def login_page():
    st.title("Login Aplikasi")
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

# --- 2. CSS Biar Mirip Swing ---
st.markdown("""
<style>
.block-container {padding-top: 2rem;}
    h2 {text-align: center; color: #1E3A8A; font-weight: 700;}
.stButton > button {
        border-radius: 4px; border: 1px solid #999;
        background-color: #EFEFEF; color: black;
    }
.stButton > button[kind="primary"] {
        background-color: #4A90E2; color: white; border: none;
    }
    div[data-testid="column"]:nth-of-type(2).stButton > button {
        width: 100%; height: 70px; font-weight: bold; color: white;
        border: none; border-radius: 8px; margin-top: 10px; font-size: 16px;
    }
    #btn-tambah button { background-color: #4CAF50; }
    #btn-update button { background-color: #2196F3; }
    #btn-hapus button { background-color: #F44336; }
    #btn-bubble button { background-color: #9C27B0; }
    #btn-merge button { background-color: #FF9800; }
.stDataFrame {border: 1px solid #AAA;}
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR MENU ---
with st.sidebar:
    st.write(f"Login sebagai: **{st.session_state.role}**")
    st.write(f"Role: {st.session_state.role}")
    if st.button("Logout"):
        st.session_state.login = False
        st.rerun()
    
    st.divider()
    st.subheader("Menu Admin")
    menu = st.selectbox("Pilih Menu", ["Tampilkan Semua", "Backup Data"], label_visibility="collapsed")
    
    st.divider()
    with st.expander("🔽 Backup Data"):
        df_backup = pd.DataFrame(st.session_state.get('data', []))
        st.download_button("Download JSON", df_backup.to_json(orient="records"), "data_mahasiswa.json")

# --- 4. Fungsi Sorting ---
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
