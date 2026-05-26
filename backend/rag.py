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

with open("../data/cloudinvent_docs.txt", "r", encoding="utf-8") as f:

    knowledge_base = f.read()

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

def ask_question(question):

    context = retrieve_context(question)

    prompt = f"""
You are CloudInvent AI Copilot.

Use ONLY the context below.

Context:
{context}

Question:
{question}

Answer professionally.
"""

    completion = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3,
    )

    return completion.choices[0].message.content