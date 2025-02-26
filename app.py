import streamlit as st
import os
import time
import tempfile

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()

# Set page configuration for dark mode
st.set_page_config(
    page_title="PDF Q&A Chatbot",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS for dark mode and footer placement
st.markdown("""
<style>
/* Set dark background and light text */
body {
    background-color: #121212;
    color: #E0E0E0;
    font-family: 'Helvetica Neue', sans-serif;
}

/* Main container styling */
.main-container {
    padding: 20px;
    margin: 20px;
}

/* Header styling */
.header {
    font-size: 2.5em;
    font-weight: bold;
    color: #FFFFFF;
    text-align: center;
    margin-bottom: 20px;
}

/* Sidebar customization */
[data-testid="stSidebar"] {
    background-color: #1E1E1E;
}

/* Button styling */
div.stButton > button {
    background-color: #BB86FC;
    color: #121212;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
    font-size: 1em;
    transition: background-color 0.3s ease;
}
div.stButton > button:hover {
    background-color: #9B59B6;
}

/* Text input styling */
div.stTextInput > div > div > input {
    border-radius: 8px;
    border: 1px solid #333333;
    padding: 10px;
    background-color: #1E1E1E;
    color: #E0E0E0;
}

/* Make the chat input area appear fixed at the bottom */
.chat-footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background: #1E1E1E;
    padding: 10px;
    border-top: 1px solid #333333;
    z-index: 100;
}
</style>
""", unsafe_allow_html=True)

# Main container for app content
with st.container():
    st.markdown('<div class="header">PDF Q&A Chatbot</div>', unsafe_allow_html=True)
    st.write("Upload your PDF files below, embed them, and then chat with the app to ask questions based on their content.")

    # Load NVIDIA API key from .env file
    os.environ['NVIDIA_API_KEY'] = os.getenv('NVIDIA_API_KEY')

    # Initialize the ChatNVIDIA model for Q&A
    llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct")

    # Sidebar instructions
    st.sidebar.header("Instructions")
    st.sidebar.markdown("""
    1. **Upload PDFs:** Select one or more PDF files.
    2. **Embed Documents:** Click *Embed Documents* to process the PDFs.
    3. **Chat:** Use the chat input at the bottom to ask your questions.
    """)

    # File uploader for PDF files
    uploaded_files = st.file_uploader("Upload one or more PDF files", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        if "documents" not in st.session_state:
            st.session_state.documents = []
        for uploaded_file in uploaded_files:
            # Avoid reprocessing the same file
            if uploaded_file.name not in [doc["name"] for doc in st.session_state.documents]:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name
                loader = PyPDFLoader(tmp_file_path)
                docs = loader.load()
                st.session_state.documents.append({"name": uploaded_file.name, "docs": docs})
        st.success("Uploaded and processed PDF file(s).")

    # Two-column layout for document embedding process
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Embed Documents"):
            if "documents" not in st.session_state or not st.session_state.documents:
                st.warning("Please upload PDF files first!")
            else:
                with st.spinner("Embedding documents..."):
                    all_docs = []
                    for item in st.session_state.documents:
                        all_docs.extend(item["docs"])
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
                    final_documents = text_splitter.split_documents(all_docs)
                    embeddings = NVIDIAEmbeddings()
                    vectorstore = FAISS.from_documents(final_documents, embeddings)
                    st.session_state.final_documents = final_documents
                    st.session_state.vectorstore = vectorstore
                    st.success("Documents embedded successfully!")
    with col2:
        st.write("You can view embedding status or logs here if needed.")

# Add a spacer so content doesn't overlap with fixed footer
st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)

# Chat input area at the bottom
# We simulate a fixed footer using custom CSS.
with st.container():
    st.markdown('<div class="chat-footer">', unsafe_allow_html=True)
    question = st.text_input("Enter your question based on the uploaded PDFs:", key="chat_input")
    if question:
        if "vectorstore" not in st.session_state:
            st.warning("Please upload and embed documents first!")
        else:
            with st.spinner("Processing your query..."):
                prompt_template = ChatPromptTemplate.from_template(
                    """
                    Answer the questions based on the provided context only.
                    Please provide the most accurate response based on the question.
                    <context>
                    {context}
                    <context>
                    Question: {input}
                    """
                )
                document_chain = create_stuff_documents_chain(llm, prompt_template)
                retriever = st.session_state.vectorstore.as_retriever()
                retrieval_chain = create_retrieval_chain(retriever, document_chain)
                start = time.process_time()
                response = retrieval_chain.invoke({"input": question})
                elapsed = time.process_time() - start
                st.write(f"Response time: {elapsed:.2f} seconds")
                st.subheader("Answer:")
                st.write(response["answer"])
                
                with st.expander("Relevant Document Excerpts"):
                    for i, doc in enumerate(response["context"]):
                        st.write(f"Chunk {i+1}:")
                        st.write(doc.page_content)
                        st.write("---")
    st.markdown('</div>', unsafe_allow_html=True)
