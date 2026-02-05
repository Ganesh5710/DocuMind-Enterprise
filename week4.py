# -----------------------------
# IMPORTS
# -----------------------------
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough

# -----------------------------
# FASTAPI APP
# -----------------------------
app = FastAPI(title="DocMind Enterprise - Week 4")

# -----------------------------
# INPUT SCHEMA
# -----------------------------
class QueryRequest(BaseModel):
    question: str

# -----------------------------
# MOCK RETRIEVER (SIMULATES VECTOR DB)
# (In real project → Pinecone / FAISS)
# -----------------------------
def retriever(query: str):
    docs = [
        Document(
            page_content="Refunds can be requested within 30 days of purchase.",
            metadata={"source": "Refund_Policy.pdf", "page": 2}
        ),
        Document(
            page_content="Accounts are activated within 24 hours after verification.",
            metadata={"source": "Account_Guide.pdf", "page": 1}
        )
    ]
    return docs

# -----------------------------
# LLM INITIALIZATION
# -----------------------------
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

# -----------------------------
# PROMPT TEMPLATE
# -----------------------------
def build_prompt(question, docs):
    context = "\n".join([doc.page_content for doc in docs])
    return f"""
You are an enterprise assistant.
Answer ONLY using the context below.
If answer not found, say "Information not available".

Context:
{context}

Question:
{question}
"""

# -----------------------------
# CHAT ENDPOINT (RAG)
# -----------------------------
@app.post("/chat")
def chat(request: QueryRequest):

    # Step 1: Retrieve documents
    docs = retriever(request.question)

    # Step 2: Build prompt with context
    prompt = build_prompt(request.question, docs)

    # Step 3: Get answer from LLM
    response = llm.invoke(prompt)

    # Step 4: Extract sources
    sources = [
        {
            "document": doc.metadata["source"],
            "page": doc.metadata["page"]
        }
        for doc in docs
    ]

    return JSONResponse(
        content={
            "answer": response.content,
            "sources": sources
        }
    )
