import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000"

# ---------- API CALLS ----------
def upload_document(file):
    if file is None:
        return "⚠️ Please select a document."

    with open(file.name, "rb") as f:
        res = requests.post(
            f"{API_URL}/upload",
            files={"file": f}
        )

    data = res.json()
    if "error" in data:
        return f"❌ {data['error']}"

    return "✅ Document uploaded successfully"

def ask_question(question):
    if not question.strip():
        return "⚠️ Please enter a question."

    res = requests.get(
        f"{API_URL}/ask",
        params={"query": question}
    )
    return res.json()["answer"]

# ---------- UI ----------
with gr.Blocks() as ui:
    gr.Markdown("## 📄 Document Question Answering Chatbot (RAG)")
    gr.Markdown(
        "Upload a **TXT, PDF, or Excel (.xlsx)** document and ask questions answered **only from the document content**."
    )

    file_input = gr.File(
        label="Upload document",
        file_types=[".txt", ".pdf", ".xlsx"]
    )

    upload_btn = gr.Button("Upload Document")
    upload_status = gr.Markdown()

    upload_btn.click(
        upload_document,
        inputs=file_input,
        outputs=upload_status
    )

    gr.Markdown("---")

    gr.Markdown("### Ask a Question")

    query_input = gr.Textbox(
        label="Your Question",
        placeholder="Ask a question based on the uploaded document"
    )

    ask_btn = gr.Button("Ask")

    answer_output = gr.Textbox(
        label="Answer",
        lines=6,
        interactive=False
    )

    ask_btn.click(
        ask_question,
        inputs=query_input,
        outputs=answer_output
    )

ui.launch()
