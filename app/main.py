from fastapi import FastAPI, UploadFile
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import PyPDFLoader
import pandas as pd
import tempfile
import os

# ---------------- ENV ----------------
load_dotenv()

# ---------------- APP ----------------
app = FastAPI()

# ================== EMBEDDINGS ==================
class STEmbedding(Embeddings):
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode([text])[0].tolist()

embedding_function = STEmbedding()

# ================== VECTOR STORE ==================
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_function,
    collection_name="documents"
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# ================== LLM ==================
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# ================== PROMPT ==================
prompt = ChatPromptTemplate.from_template(
    """
    Answer the question using the context below.

    If the context clearly describes or explains the concept asked about,
    you may answer even if the exact wording of the question is not present.

    Do NOT use outside knowledge.
    If the answer cannot be reasonably inferred from the context, say:
    "I don't know based on the provided document."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
)



# ================== HELPERS ==================
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# ================== RAG CHAIN ==================
rag_chain = (
    {
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
)

# ================== TEXT SPLITTER ==================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", ".", " ", ""]
)

# ================== API ==================
@app.post("/upload")
async def upload_file(file: UploadFile):
    filename = file.filename.lower()

    # ---------- TXT ----------
    if filename.endswith(".txt"):
        content = await file.read()
        text = content.decode("utf-8")
        chunks = text_splitter.split_text(text)

    # ---------- PDF ----------
    elif filename.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        loader = PyPDFLoader(tmp_path)
        docs = loader.load()
        text = "\n".join(doc.page_content for doc in docs)
        chunks = text_splitter.split_text(text)

        os.remove(tmp_path)

    # ---------- EXCEL ----------
    elif filename.endswith(".xlsx"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        df = pd.read_excel(tmp_path)

        # Convert rows to readable text
        rows_as_text = []
        for _, row in df.iterrows():
            row_text = " | ".join(
                f"{col}: {row[col]}" for col in df.columns
            )
            rows_as_text.append(row_text)

        text = "\n".join(rows_as_text)
        chunks = text_splitter.split_text(text)

        os.remove(tmp_path)

    else:
        return {"error": "Supported formats: .txt, .pdf, .xlsx"}

    metadatas = [{"source": file.filename}] * len(chunks)
    vectorstore.add_texts(texts=chunks, metadatas=metadatas)

    return {"message": "Document uploaded successfully"}

@app.get("/ask")
def ask(query: str):
    response = rag_chain.invoke(query)
    return {"answer": response.content}
