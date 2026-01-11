Step 1️⃣: Create README.md in project root

Create a file named:

README.md

Step 2️⃣: Paste this (carefully written for YOU)

Copy–paste the following exactly (you can tweak later):

# 📄 Document Question Answering Chatbot using RAG

This project implements a **document-based question answering chatbot** using a **Retrieval-Augmented Generation (RAG)** approach. Users can upload documents and ask natural language questions, and the system answers **strictly based on the uploaded content**, minimizing hallucinations.

---

## 🚀 Features

- Upload and query **TXT, PDF, and Excel (.xlsx)** documents  
- Semantic document retrieval using **vector embeddings**
- Context-grounded answer generation using a large language model
- Explicit hallucination control ("I don't know" when context is insufficient)
- Simple web interface for document upload and querying

---

## 🧠 System Architecture (High Level)

1. Uploaded documents are split into overlapping text chunks
2. Each chunk is converted into a vector embedding
3. Embeddings are stored in a vector database (ChromaDB)
4. For a user query:
   - Relevant chunks are retrieved using semantic similarity
   - Retrieved context is passed to the language model
   - The model generates an answer strictly from the context

---

## 🛠 Tech Stack

- **Backend**: FastAPI  
- **UI**: Gradio  
- **RAG Framework**: LangChain  
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)  
- **Vector Database**: ChromaDB  
- **LLM**: LLaMA-3 (via Groq API)  

---

## 🧩 Project Structure



document-rag-chatbot/
│
├── app/
│ └── main.py # FastAPI backend (RAG pipeline)
│
├── ui/
│ └── gradio_app.py # Gradio-based user interface
│
├── chroma_db/ # Vector database (generated at runtime)
│
├── requirements.txt
├── .gitignore
└── README.md


---

## ▶️ Running the Project Locally

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/document-rag-chatbot.git
cd document-rag-chatbot

2. Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Set environment variables

Create a .env file and add:

GROQ_API_KEY=your_api_key_here

4. Start the backend
uvicorn app.main:app --reload

5. Start the UI
python ui/gradio_app.py


Open the UI in your browser and start querying your documents.

📌 Notes

The system answers only from the uploaded documents

If the answer is not present or cannot be inferred from context, the chatbot explicitly responds with "I don't know based on the provided document."

🔮 Future Improvements

Source citation for answers

Persistent user sessions

Cloud deployment

Authentication and access control
