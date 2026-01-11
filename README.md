# 📄 Document Question Answering Chatbot using RAG

This project is a **Document-based Question Answering chatbot** built using the **Retrieval-Augmented Generation (RAG)** approach.  
Users can upload documents and ask natural language questions, and the system generates **context-grounded answers strictly from the uploaded content**.

---

## 🚀 Features

- Upload and process **TXT, PDF, and Excel (.xlsx)** documents
- Automatic document **chunking and semantic indexing**
- **Semantic search** using vector embeddings
- Context-aware answers generated using a Large Language Model
- Explicit **hallucination control** (answers only from document context)
- Interactive **web-based UI**

---

## 🧠 Architecture Overview

1. **Document Ingestion**
   - Documents are uploaded via the UI
   - Text is extracted and split into overlapping chunks

2. **Embedding & Storage**
   - Chunks are converted into vector embeddings using Sentence Transformers
   - Embeddings are stored in **ChromaDB** for fast semantic retrieval

3. **Retrieval-Augmented Generation**
   - Relevant chunks are retrieved based on semantic similarity
   - Retrieved context is passed to the LLM with a strict prompt
   - The LLM generates answers grounded only in the document content

---

## 🛠️ Tech Stack

| Component | Technology |
|---------|-----------|
| Backend API | FastAPI |
| UI | Gradio |
| RAG Framework | LangChain |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| LLM | Groq (LLaMA-3.1) |
| Language | Python |

---

## 📂 Supported File Types

- `.txt` – Plain text documents  
- `.pdf` – Multi-page PDF files  
- `.xlsx` – Excel sheets (row-wise semantic indexing)

---

## ⚠️ Hallucination Control

The chatbot is **explicitly instructed** to:
- Use **only the retrieved document context**
- Respond with *"I don't know based on the provided document"* if the answer cannot be inferred

This ensures reliable and document-grounded responses.

---
