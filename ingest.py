import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

PDF_FOLDER = "data/pdfs"

# ✅ Check if folder exists
if not os.path.exists(PDF_FOLDER):
 print("Looking for folder at:", os.path.abspath(PDF_FOLDER))


documents = []

# ✅ Load PDFs safely
for file in os.listdir(PDF_FOLDER):
    if file.lower().endswith(".pdf"):
        file_path = os.path.join(PDF_FOLDER, file)
        print(f"Loading: {file_path}")
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())

if not documents:
    raise ValueError("No PDF documents found in folder.")

# ✅ Split text
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print(f"Total chunks created: {len(chunks)}")

# ✅ Initialize embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# ✅ Create Chroma DB
db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

# Persist database
db.persist()

print("✅ PDFs successfully ingested into ChromaDB")
print(f"Total chunks stored: {len(chunks)}")

