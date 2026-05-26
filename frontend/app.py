import streamlit as st
import requests
import os
from PIL import Image


# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="CloudInvent AI Copilot",
    layout="wide"
)

API_URL = "https://cloudinvent-backend.onrender.com/chat"

# ======================================================
# TITLE
# ======================================================

st.title("☁️ CloudInvent AI Copilot")



# ======================================================
# LOGO
# ======================================================

current_dir = os.path.dirname(__file__)

logo_path = os.path.join(
    current_dir,
    "logo.png"
)

if os.path.exists(logo_path):

    logo = Image.open(logo_path)

    st.image(logo, width=180)

else:

    st.warning(
        f"Logo not found at: {logo_path}"
    )






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

prompt = sample_prompt

user_input = st.chat_input(
    "Ask anything about CloudInvent"
)

# ======================================================
# BUTTON
# ======================================================

if st.button("Ask"):

    if prompt:

        with st.spinner("Thinking..."):

            try:

                response = requests.post(

                    API_URL,

                    json={
                        "question": prompt
                    },

                    timeout=120
                )

                # DEBUGGING
                st.write("Status Code:", response.status_code)

                st.write("Raw Response:")

                st.code(response.text)

                # JSON PARSE
                data = response.json()

                # SHOW ANSWER
                st.success(data["answer"])

            except Exception as e:

                st.error(f"Error: {e}")



# ======================================================
# USE SAMPLE QUESTION
# ======================================================

if user_input:

    prompt = user_input

# ======================================================
# PROCESS QUESTION
# ======================================================

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        try:

            files = None

            if uploaded_file:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        "application/pdf"
                    )
                }

            # ======================================================
            # BACKEND API
            # ======================================================

            payload = {
            "question": str(prompt)
            }

            response = requests.post(

            API_URL,

            json=payload,

            headers={
            "Content-Type": "application/json"
            },

            timeout=120
            )
            #answer = response.json()["answer"]
            #st.markdown(answer)

            #data = response.json()
            #st.write(data["answer"])

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": data["answer"]
                }
            )

        except Exception as e:

            st.error(str(e))


# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.caption(
    "Powered by Groq + Llama 3 + FastAPI + Streamlit"
)