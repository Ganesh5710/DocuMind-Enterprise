# -----------------------------
# IMPORTS
# -----------------------------
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from langchain_openai import ChatOpenAI

# -----------------------------
# FASTAPI APP
# -----------------------------
app = FastAPI(title="DocMind Enterprise - Week 3")

# -----------------------------
# INPUT SCHEMA
# -----------------------------
class QueryRequest(BaseModel):
    question: str

# -----------------------------
# LLM INITIALIZATION
# -----------------------------
# Make sure OPENAI_API_KEY is set in environment variables
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    streaming=True   # VERY IMPORTANT for Week-3
)

# -----------------------------
# HOME ENDPOINT
# -----------------------------
@app.get("/")
def home():
    return {"message": "DocMind API is running (Week-3)"}

# -----------------------------
# STREAMING GENERATOR FUNCTION
# -----------------------------
def stream_answer(question: str):
    """
    This function streams the answer token-by-token
    """
    for chunk in llm.stream(question):
        if chunk.content:
            yield chunk.content

# -----------------------------
# CHAT ENDPOINT (STREAMING)
# -----------------------------
@app.post("/chat")
def chat(request: QueryRequest):
    return StreamingResponse(
        stream_answer(request.question),
        media_type="text/plain"
    )

