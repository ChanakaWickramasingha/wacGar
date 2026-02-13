import streamlit as st

from api import predict_garbage
from api import signup_user
from api import login_user
import base64

st.set_page_config(page_title="Garbage Classifier", layout="centered")

# ---------------- SESSION STATE ----------------
if "token" not in st.session_state:
    st.session_state.token = None
if "page" not in st.session_state:
    st.session_state.page = "login"  # login | signup


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


# ---------------- SIGNUP PAGE ----------------
def signup_page():
    st.title("Sign Up")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if not email or not password or not confirm_password:
            st.warning("Please fill all fields")
            return

        if password != confirm_password:
            st.error("Passwords do not match")
            return

        response = signup_user(email, password)

        if response.status_code == 200:
            st.success("Account created successfully 🎉")
            st.info("Please login now")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error(response.json().get("detail", "Signup failed"))

    st.write("Already have an account?")
    if st.button("Go to Login"):
        st.session_state.page = "login"
        st.rerun()


# ---------------- LOGIN PAGE ----------------
# login_page()


def login_page():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

   # Buttons
    col1, col2 = st.columns(2, gap="small")

    with col1:
        if st.button("Login", use_container_width=True, key="login_btn"):
            if not email or not password:
                st.warning("⚠️ Please fill all fields")

                # Assuming you have a login_user function
            response = login_user(email, password)

            if response.status_code == 200:
                data = response.json()
                st.session_state.token = data["access_token"]
                st.success("🎉 Login successful!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Invalid email or password")

    with col2:
        if st.button("Sign Up", key="signup_btn", use_container_width=True):
            st.session_state.page = "signup"
            st.rerun()


# ---------------- DASHBOARD ----------------
def dashboard():
    # ================== SIDEBAR ==================
    with st.sidebar:
        st.title("♻️ WAC AI")
        st.markdown("### Model Info")
        st.info("Deep Learning Image Classifier")
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.token = None
            st.rerun()

    # ================== HEADER ==================
    col_logo, col_title = st.columns([1, 8])

    with col_logo:
        st.markdown(
            """
            <div style="display:flex; align-items:center; height:90px;">
                <img src="data:image/png;base64,{img_base64}" width="70">
            </div>
            """.format(img_base64=get_base64_image("assets/wacgreen.png")),
            unsafe_allow_html=True
        )

    with col_title:
        st.markdown(
            """
            <div style="display:flex; align-items:center; height:90px;">
                <h1 style="margin:0;">WAC Green AI</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "<p style='color:gray; margin-top:-10px;'>Upload an image to classify garbage type using AI.</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ================== MAIN LAYOUT ==================
    col1, col2 = st.columns([1, 1.2])

    # -------- LEFT SIDE: IMAGE UPLOAD --------
    with col1:
        # Upload Header (Icon + Text aligned)
        up_col1, up_col2 = st.columns([0.15, 0.85])

        with up_col1:
            st.image("assets/upload.png", width=35)

        with up_col2:
            st.markdown(
                "<h4 style='margin-bottom:0;'>Upload Image</h4>",
                unsafe_allow_html=True
            )

        st.markdown("<div style='margin-top:-10px;'></div>",
                    unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file:
            st.image(uploaded_file, use_column_width=True)

        if st.button("Run Classification", use_container_width=True):
            with st.spinner("Analyzing image with AI model..."):
                response = predict_garbage(
                    uploaded_file,
                    st.session_state.token
                )

            if response.status_code == 200:
                st.session_state.result = response.json()
            else:
                st.error("Prediction failed. Please try again.")

    # -------- RIGHT SIDE: RESULTS --------
    with col2:
        st.subheader("Model Results")

        if "result" in st.session_state:

            result = st.session_state.result

            st.success("Classification Complete")

            # Garbage Type
            st.markdown("### Predicted Class")
            st.markdown(
                f"<h2 style='color:green;'>{result['class'].upper()}</h2>",
                unsafe_allow_html=True
            )

            # Confidence as metric
            st.markdown("### Confidence Score")
            confidence = float(result["confidence"])
            st.metric(
                label="Model Confidence",
                value=f"{confidence*100:.2f}%"
            )
            st.progress(confidence)

            st.markdown("---")

            # Explanation
            st.markdown("### AI Explanation")
            st.info(result["description"])

            # tips
            st.markdown("### ♻️ Recycling Tips")
            tips_html = "".join(
                [f"<li style='margin-bottom:8px;'>{tip}</li>"
                 for tip in result["recycling_tips"]]
            )

            st.markdown(
                f"""
                <div style="
                    background-color:#f8f9fa;
                    padding:15px;
                    border-radius:8px;
                ">
                    <ul style="margin:0; padding-left:20px;">
                        {tips_html}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.info("Upload an image and run classification to see results.")


# ---------------- ROUTING ----------------
if st.session_state.token:
    dashboard()
else:
    if st.session_state.page == "signup":
        signup_page()
    else:
        login_page()
