import streamlit as st
import requests
import os

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="CloudInvent AI Copilot",
    layout="wide"
)

# ======================================================
# LOGO
# ======================================================

logo_path = os.path.join(
    os.path.dirname(__file__),
    "logo.png"
)

if os.path.exists(logo_path):

    st.image(logo_path, width=180)

# ======================================================
# TITLE
# ======================================================

st.title("☁️ CloudInvent AI Copilot")

# ======================================================
# SIMPLE LOGIN
# ======================================================

APP_PASSWORD = "cloudinvent123"

password = st.sidebar.text_input(
    "Enter Password",
    type="password"
)

if password != APP_PASSWORD:

    st.warning("Please enter password.")

    st.stop()

# ======================================================
# CHAT HISTORY
# ======================================================

if "messages" not in st.session_state:

    st.session_state.messages = []

# ======================================================
# DISPLAY CHAT HISTORY
# ======================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ======================================================
# PDF UPLOAD
# ======================================================

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# ======================================================
# SAMPLE QUESTIONS
# ======================================================

st.markdown("### 🚀 Try Sample Questions")

sample_prompt = None

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "☁️ What does CloudInvent do?",
        use_container_width=True
    ):

        sample_prompt = (
            "What does CloudInvent do?"
        )

    if st.button(
        "💰 Explain FinOps capabilities",
        use_container_width=True
    ):

        sample_prompt = (
            "Explain CloudInvent FinOps capabilities"
        )

with col2:

    if st.button(
        "📉 How are cloud costs optimized?",
        use_container_width=True
    ):

        sample_prompt = (
            "How does CloudInvent optimize cloud costs?"
        )

    if st.button(
        "🔐 Explain governance and security",
        use_container_width=True
    ):

        sample_prompt = (
            "Explain CloudInvent governance and security capabilities"
        )

# ======================================================
# CHAT INPUT
# ======================================================

prompt = st.chat_input(
    "Ask anything about CloudInvent"
)

# ======================================================
# USE SAMPLE QUESTION
# ======================================================

if sample_prompt:

    prompt = sample_prompt

# ======================================================
# PROCESS QUESTION
# ======================================================

if prompt:

    # ==================================================
    # ADD USER MESSAGE
    # ==================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    # ==================================================
    # ASSISTANT RESPONSE
    # ==================================================

    with st.chat_message("assistant"):

        try:

            # ==========================================
            # BACKEND API
            # ==========================================

            API_URL = (
                "https://chatassist-backend-auta.onrender.com/chat"
            )

            # ==========================================
            # API CALL
            # ==========================================

            response = requests.post(

                API_URL,

                json={
                    "question": prompt
                },

                timeout=120
            )

            # ==========================================
            # DEBUGGING
            # ==========================================

            st.sidebar.markdown("### Debug Info")

            st.sidebar.write(
                f"Status Code: {response.status_code}"
            )

            # ==========================================
            # VALIDATE RESPONSE
            # ==========================================

            if response.status_code != 200:

                st.error(
                    f"Backend Error: {response.text}"
                )

                st.stop()

            # ==========================================
            # SAFE JSON PARSING
            # ==========================================

            try:

                data = response.json()

            except Exception:

                st.error(
                    "Invalid JSON response from backend."
                )

                st.code(response.text)

                st.stop()

            # ==========================================
            # GET ANSWER
            # ==========================================

            answer = data.get(
                "answer",
                "No answer returned."
            )

            # ==========================================
            # DISPLAY ANSWER
            # ==========================================

            st.markdown(answer)

            # ==========================================
            # SAVE CHAT HISTORY
            # ==========================================

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except requests.exceptions.Timeout:

            st.error(
                "Request timed out. Render free tier may be waking up."
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to backend service."
            )

        except Exception as e:

            st.error(
                f"Unexpected Error: {str(e)}"
            )

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.caption(
    "Powered by Groq + Llama 3 + FastAPI + Streamlit"
)