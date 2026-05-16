import streamlit as st
import hashlib
import base64
from utils.database import fetchone, run, get_media, save_media, delete_media
from datetime import datetime


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


def create_default_admin():
    existing = fetchone("SELECT id FROM users WHERE username='admin'")
    if not existing:
        run("INSERT INTO users (username,password_hash,full_name,role,email,is_active) VALUES (%s,%s,%s,%s,%s,%s)",
            ('admin', hash_password('admin123'), 'Administrator', 'admin', 'admin@pindad.com', 1))


def authenticate(username: str, password: str):
    user = fetchone("SELECT * FROM users WHERE username=%s AND is_active=1", (username,))
    if user and verify_password(password, user['password_hash']):
        run("UPDATE users SET last_login=%s WHERE id=%s",
            (datetime.now().isoformat(), user['id']))
        return user
    return None


def get_login_logo_b64():
    try:
        row = get_media('login_logo')
        if row and row['data']:
            return "data:" + row['mime_type'] + ";base64," + row['data']
    except Exception:
        pass
    return None


def save_login_logo(file_bytes, mime_type, filename):
    b64 = base64.b64encode(file_bytes).decode()
    save_media('login_logo', filename, b64, mime_type)


def delete_login_logo():
    delete_media('login_logo')


def is_admin():
    return st.session_state.get('role') == 'admin'


def require_admin():
    if not is_admin():
        st.error("Akses ditolak. Fitur ini hanya untuk Admin.")
        st.stop()


def logout():
    for key in ['logged_in', 'user', 'role']:
        st.session_state.pop(key, None)
    st.rerun()
