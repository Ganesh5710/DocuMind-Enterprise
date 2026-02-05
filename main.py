from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Input schema
class QueryRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "DocMind API is running"}

@app.post("/chat")
def chat(request: QueryRequest):
    return {"you_asked": request.question}
