from fastapi import FastAPI, UploadFile, File, Form
from rag import ask_question
from pypdf import PdfReader
import tempfile


from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from rag import ask_question



app = FastAPI()

# ======================================================
# HOME
# ======================================================

@app.get("/")
def home():

    return {
        "message": "CloudInvent AI Copilot Backend Running"
    }

# ======================================================
# CHAT API
# ======================================================

@app.post("/chat")
async def chat(

    question: str = Form(...),

    file: UploadFile = File(None)

):

    pdf_text = ""

    # ==================================================
    # PROCESS PDF
    # ==================================================

    if file:

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                contents = await file.read()

                temp_file.write(contents)

                temp_path = temp_file.name

            reader = PdfReader(temp_path)

            for page in reader.pages:

                extracted = page.extract_text()

                if extracted:

                    pdf_text += extracted + "\n"

        except Exception as e:

            pdf_text = f"PDF processing error: {str(e)}"

    # ==================================================
    # ASK QUESTION
    # ==================================================

    answer = ask_question(
        question,
        pdf_text
    )

    return {
        "answer": answer
    }


# ======================================================
# CORS
# ======================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# REQUEST MODEL
# ======================================================

class QuestionRequest(BaseModel):

    question: str

# ======================================================
# HEALTH CHECK
# ======================================================

@app.get("/")

def root():

    return {
        "status": "CloudInvent AI Backend Running"
    }


# ======================================================
# CHAT ENDPOINT
# ======================================================

@app.post("/chat")

def chat(request: QuestionRequest):

    answer = ask_question(request.question)

    return {
        "answer": answer
    }