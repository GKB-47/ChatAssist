from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from groq import Groq
from dotenv import load_dotenv
import os

# =========================================================
# LOAD ENV VARIABLES
# =========================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# =========================================================
# GROQ CLIENT
# =========================================================

client = Groq(
    api_key=GROQ_API_KEY
)

# =========================================================
# EMBEDDING MODEL
# =========================================================

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================================================
# CHROMA VECTOR DATABASE
# =========================================================

db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding
)

# =========================================================
# MAIN CHAT FUNCTION
# =========================================================

def ask_question(question, pdf_text="", history=None):

    try:

        # =================================================
        # RETRIEVE DOCUMENTS
        # =================================================

        docs = db.similarity_search(question, k=4)

        # =================================================
        # BUILD CONTEXT
        # =================================================

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        # =================================================
        # SOURCE CITATIONS
        # =================================================

        sources = []

        for doc in docs:

            source = doc.metadata.get(
                "source",
                "CloudInvent Knowledge Base"
            )

            sources.append(source)

        unique_sources = list(set(sources))

        # =================================================
        # CHAT HISTORY
        # =================================================

        history_text = ""

        if history:

            recent_history = history[-6:]

            for msg in recent_history:

                role = msg.get("role", "user")
                content = msg.get("content", "")

                history_text += f"{role}: {content}\n"

        # =================================================
        # ENTERPRISE PROMPT
        # =================================================

        if not context.strip():

            return (
            "I could not find this information "
            "in the CloudInvent knowledge base."
            )


        prompt = f"""
        You are CloudInvent AI Copilot.

        Your role:
        - Explain CloudInvent services and capabilities
        - Help with FinOps and cloud optimization
        - Explain governance, compliance, and security
        - Assist with AWS, Azure, and GCP topics
        - Answer professionally like an enterprise consultant

        Behavior Guidelines:
        - Use ONLY the provided context
        - Never hallucinate information
        - If answer is unavailable, clearly say:
        'I could not find this information in the CloudInvent knowledge base.'
        - Be concise but informative
        - Use bullet points where appropriate
        - Format responses professionally
        - Prioritize clarity and accuracy

        Conversation History:
        {history_text}

        PDF Context:
        {pdf_text}

        Knowledge Base Context:
        {context}

        User Question:
        {question}

        Provide a professional response below:
        """

      

        # =================================================
        # GROQ API CALL WITH STREAMING
        # =================================================

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3,

            max_tokens=1024,

            stream=True
        )

        # =================================================
        # STREAM RESPONSE
        # =================================================

        final_answer = ""

        for chunk in response:

            if chunk.choices[0].delta.content:

                final_answer += chunk.choices[0].delta.content

        # =================================================
        # ADD SOURCES
        # =================================================

        if unique_sources:

            final_answer += "\n\n---\n\nSources:\n"

            for src in unique_sources:

                final_answer += f"- {src}\n"

        return final_answer

    except Exception as e:

        return f"Error generating response: {str(e)}"