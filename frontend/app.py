import streamlit as st
import requests

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="CloudInvent AI Copilot",
    page_icon="☁️",
    layout="wide"
)

# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.stTextInput > div > div > input {
    font-size: 16px;
}

.sample-question button {
    width: 100%;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# TITLE
# ======================================================

st.title("☁️ CloudInvent AI Copilot")

st.markdown("""
Ask questions about:

- Cloud FinOps
- Cloud Cost Optimization
- Governance
- Cloud Migration
- AI Solutions
- CloudInvent Services
""")

# ======================================================
# BACKEND API
# ======================================================

API_URL = "https://chatassist-backend-auta.onrender.com/chat"
#API_URL = "http://localhost:8000/chat"
#API_URL = "https://127.0.0.1/chat"

# ======================================================
# SESSION STATE
# ======================================================

if "question" not in st.session_state:
    st.session_state.question = ""

# ======================================================
# SAMPLE QUESTIONS
# ======================================================

st.subheader("💡 Sample Questions")

col1, col2 = st.columns(2)

with col1:

    if st.button("What services does CloudInvent provide?"):
        st.session_state.question = (
            "What services does CloudInvent provide?"
        )

    if st.button("How does CloudInvent help optimize cloud costs?"):
        st.session_state.question = (
            "How does CloudInvent help optimize cloud costs?"
        )

with col2:

    if st.button("What is Cloud FinOps?"):
        st.session_state.question = (
            "What is Cloud FinOps?"
        )

    if st.button("Tell me about CloudInvent AI solutions"):
        st.session_state.question = (
            "Tell me about CloudInvent AI solutions"
        )

# ======================================================
# USER INPUT
# ======================================================

prompt = st.text_input(
    "Enter your question",
    value=st.session_state.question
)

# ======================================================
# ASK BUTTON
# ======================================================

if st.button("Ask AI"):

    if not prompt.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            try:

                response = requests.post(

                    API_URL,

                    json={
                        "question": prompt
                    },

                    timeout=120
                )

                # ======================================================
                # DEBUG INFO
                # ======================================================

                st.write("### Debug Info")

                st.write(
                    f"Status Code: {response.status_code}"
                )

                st.write("Raw Response:")

                st.code(response.text)

                # ======================================================
                # CHECK RESPONSE
                # ======================================================

                if response.status_code == 200:

                    data = response.json()

                    answer = data.get(
                        "answer",
                        "No answer returned."
                    )

                    st.success("Answer")

                    st.write(answer)

                else:

                    st.error(
                        "Backend returned an error."
                    )

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.caption(
    "Powered by Groq + Llama 3 + FastAPI + Streamlit"
)