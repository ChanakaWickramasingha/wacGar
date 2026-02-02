import streamlit as st
from api import login_user
from api import predict_garbage

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
    st.title("♻️ Garbage Classification")

    st.write("Upload an image of garbage to classify it.")

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        if st.button("Classify Garbage"):
            with st.spinner("Analyzing image..."):
                response = predict_garbage(uploaded_file, st.session_state.token)

            if response.status_code == 200:
                result = response.json()

                st.success("Classification Complete ✅")

                st.subheader("🗑️ Garbage Type")
                st.write(f"**{result['class'].upper()}**")

                st.subheader("📊 Confidence")
                st.progress(result["confidence"])

                st.subheader("🧠 AI Explanation")
                st.write(result["description"])

                st.subheader("♻️ Recycling Tips")
                for tip in result["recycling_tips"]:
                    st.write(f"- {tip}")
            else:
                st.error("Prediction failed. Please try again.")

    if st.button("Logout"):
        st.session_state.token = None
        st.rerun()
# ---------------- ROUTING ----------------
if st.session_state.token:
    dashboard()
else:
    login_page()
