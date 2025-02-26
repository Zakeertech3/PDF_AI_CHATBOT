# PDF Q&A Chatbot 🚀

Welcome to the **PDF Q&A Chatbot!** This interactive, Streamlit-based application helps you extract information from PDFs using natural language queries. Whether you're a researcher, professional, or just curious, this tool makes it easy to search through lengthy PDFs for exact details.

---

## Overview 📄
### The PDF Q&A Chatbot lets you:
- 📥 **Upload** one or more PDF files directly.
- 🧩 **Embed** document contents into a searchable vector store using NVIDIA’s AI endpoints.
- 💬 **Chat** via a fixed input at the bottom of the page.
- 🔍 **Retrieve** answers with relevant document excerpts for context.

**Tip:** Ideal for research papers, business reports, legal documents, and more!

---

## Features 🔍💬
### 📥 PDF Upload:
- Drag and drop PDF files into the interface.

### 🧩 Document Embedding:
- Uses `PyPDFLoader` to process PDFs.
- Splits documents into manageable chunks using `RecursiveCharacterTextSplitter`.
- Converts chunks into vector embeddings with `NVIDIAEmbeddings`.
- Stores embeddings in a **FAISS** vector store.

### 💡 Interactive Chat:
- Ask questions in the chat input.
- Retrieves relevant document excerpts.
- Generates accurate answers using `ChatNVIDIA`.

### ⏱️ Real-Time Feedback:
- Displays response time.
- Shows relevant document excerpts.

---

## Why Use This Chatbot? 🤔
✅ **Researchers:** Quickly extract key information from academic articles.

✅ **Professionals:** Search through financial reports, legal documents, and technical manuals.

✅ **Everyone:** Easily get detailed answers from lengthy PDFs.

---

## How It Works ⚙️
1. **Upload Your PDFs**:
   - Use the file uploader to select one or more PDF files.

2. **Embed the Documents**:
   - Click the `Embed Documents` button.
   - The app processes PDFs, splits text into chunks, and stores embeddings in FAISS.

3. **Chat and Query**:
   - Enter a question in the chat input at the bottom.
   - Retrieves relevant document chunks and generates answers using `ChatNVIDIA`.

4. **View Answers and Excerpts**:
   - Displays the response along with response time and relevant document excerpts.

---

## Installation and Setup 🛠️

### **Prerequisites**
- Python **3.7+**
- **Streamlit**, **LangChain**, **FAISS**, **PyPDF**, **python-dotenv**

### **Installation Steps**

#### **Clone the Repository:**
```bash
git clone https://github.com/Zakeertech3/PDF_AI_CHATBOT.git
cd pdf-qa-chatbot
```

#### **Install Dependencies:**
```bash
pip install streamlit langchain langchain-nvidia-ai-endpoints pypdf faiss-cpu python-dotenv
```

#### **Set Up Environment Variables:**
Create a `.env` file in the project root directory with:
```ini
NVIDIA_API_KEY=your_nvidia_api_key_here
```

#### **Run the Application:**
```bash
streamlit run app.py
```

---

## Code Structure 📂

### **File Upload & Processing:**
- Uses `st.file_uploader` for PDF uploads.
- Processes files using `PyPDFLoader`.

### **Document Embedding:**
- Splits PDFs into text chunks with `RecursiveCharacterTextSplitter`.
- Converts chunks into vector embeddings with `NVIDIAEmbeddings`.
- Stores embeddings in a FAISS vector store for fast retrieval.

### **Chat Interface:**
- Fixed chat input at the bottom via custom CSS.
- Retrieves document excerpts and generates responses using `ChatNVIDIA`.

### **Custom Styling:**
- Dark-themed interface.
- Custom buttons and a fixed footer for chat.

---

## Deployment 🚀
This application is deployed on **Streamlit Cloud**.

Try it out here: **[PDF Q&A Chatbot](https://pdfaichatbot-vcds3mrdu6t5mdlqm9cmgp.streamlit.app/)**

---

## Contributing 🤝
We welcome contributions! To contribute:
1. **Fork the repository**.
2. **Create a feature branch** (`git checkout -b feature-branch`).
3. **Commit changes** (`git commit -m "Added a new feature"`).
4. **Push to GitHub** (`git push origin feature-branch`).
5. **Create a pull request**.

### **Ways to Contribute:**
- **🐛 Bug Reports**: File a bug report on GitHub.
- **💡 Feature Requests**: Open an issue to suggest improvements.

---

## License 📜
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

### 🚀 Enjoy using the PDF Q&A Chatbot!
If you have any questions or feedback, feel free to reach out. 😊
