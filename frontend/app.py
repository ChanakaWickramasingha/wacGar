import streamlit as st
from api import login_user

st.set_page_config(page_title="Garbage Classifier", layout="centered")

# ---------------- SESSION STATE ----------------
if "token" not in st.session_state:
    st.session_state.token = None

# ---------------- LOGIN PAGE ----------------
def login_page():
    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.warning("Please fill all fields")
            return

        response = login_user(email, password)

        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.success("Login successful 🎉")
            st.rerun()
        else:
            st.error("Invalid email or password")

# ---------------- DASHBOARD ----------------
def dashboard():
    st.title("♻️ Garbage Classification App")
    st.success("You are logged in")

    st.write("JWT Token (stored securely in session):")
    st.code(st.session_state.token)

    if st.button("Logout"):
        st.session_state.token = None
        st.rerun()

# ---------------- ROUTING ----------------
if st.session_state.token:
    dashboard()
else:
    login_page()
