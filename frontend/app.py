import streamlit as st
import requests
import os

st.set_page_config(
    page_title="CloudInvent AI Copilot",
    layout="wide"
)

logo_path = os.path.join(
    os.path.dirname(__file__),
    "logo.png"
)

if os.path.exists(logo_path):

    st.sidebar.image(logo_path, width=180)

# ======================================================
# SIMPLE LOGIN
# ======================================================

APP_PASSWORD = "cloudinvent123"

password = st.sidebar.text_input(
    "Enter Password",
    type="password"
)

if not password:

    st.stop()

if password != APP_PASSWORD:

    st.sidebar.error("Incorrect password")

    st.stop()


st.title("☁️ CloudInvent AI Copilot")

# ======================================================
# CHAT HISTORY
# ======================================================

if "messages" not in st.session_state:
    st.session_state.messages = []



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
# DISPLAY CHAT HISTORY
# ======================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ======================================================
# CHAT INPUT
# ======================================================

prompt = sample_prompt

user_input = st.chat_input(
    "Ask anything about CloudInvent"
)

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

            

            API_URL = "https://chatassist-backend-auta.onrender.com/chat"

            response = requests.post(
                API_URL,
                data={
                    "question": prompt
                },
                files=files if uploaded_file else None,
                timeout=120
            )

            #answer = response.json()["answer"]
            #st.markdown(answer)

            st.write("Status Code:", response.status_code)
            st.write("Raw Response:")
            st.code(response.text)
            if response.status_code != 200:
                st.stop()
            data = response.json()
            answer = data["answer"]




            st.session_state.messages.append(
                {
                    "role": "assistant",
                    #"content": answer
                }
            )

        except Exception as e:

            st.error(str(e))