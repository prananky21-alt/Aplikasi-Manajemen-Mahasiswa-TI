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
            'umur': self._umur, 'jurusan': self.jurusan, 'ip
