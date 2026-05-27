import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =====================================================
# LOAD KNOWLEDGE BASE
# =====================================================

BASE_DIR = os.path.dirname(__file__)

docs_path = os.path.join(
    BASE_DIR,
    "cloudinvent_docs.txt"
)

if os.path.exists(docs_path):

    with open(docs_path, "r", encoding="utf-8") as f:

        knowledge_base = f.read()

else:

    knowledge_base = """
    CloudInvent provides cloud migration,
    FinOps optimization,
    governance,
    security,
    and cloud transformation services.
    """

# =====================================================
# SIMPLE RETRIEVAL
# =====================================================

def retrieve_context(question):

    chunks = knowledge_base.split("\n")

    scored = []

    question_words = question.lower().split()

    for chunk in chunks:

        score = 0

        chunk_lower = chunk.lower()

        for word in question_words:

            if word in chunk_lower:

                score += 1

        scored.append((score, chunk))

    scored.sort(reverse=True)

    top_chunks = [
        chunk for score, chunk in scored[:10]
        if score > 0
    ]

    return "\n".join(top_chunks)

# =====================================================
# MAIN FUNCTION
# =====================================================

def ask_question(question, pdf_text=""):

    context = retrieve_context(question)

    prompt = f"""
    You are CloudInvent AI Copilot.

    Use ONLY the context below.

    Website Context:
    {context}

    PDF Context:
    {pdf_text}

    Question:
    {question}

    Answer professionally.
    """

    try:

        completion = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                "role": "user",
                "content": prompt
                }
            ],

            temperature=0.3,
        )

        return completion.choices[0].message.content

    except Exception as e:

        return f"Groq API Error: {str(e)}"
    

# =====================================================
# SIMPLE RETRIEVAL
# =====================================================

def retrieve_context(question):

    chunks = knowledge_base.split("\n")

    scored = []

    question_words = question.lower().split()

    for chunk in chunks:

        score = 0

        chunk_lower = chunk.lower()

        for word in question_words:

            if word in chunk_lower:
                score += 1

        scored.append((score, chunk))   

    scored.sort(reverse=True)

    top_chunks = [
        chunk for score, chunk in scored[:10]
            if score > 0
        ]

    return "\n".join(top_chunks)