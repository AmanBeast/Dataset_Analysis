"""
Document Intelligence System - Streamlit UI.

Provides an enterprise-grade presentation layer for PDF ingestion, FAISS indexing,
retrieval visualization, and ChatGroq Q&A.
"""

import time
import os
import streamlit as st
from pathlib import Path
from config.settings import Settings, logger
from services.document_service import DocumentProcessingService
from services.qa_service import RetrievalQAService
from core.exceptions import (
    DocumentIntelligenceError,
    PDFProcessingError,
    InvalidPDFError,
    EmptyPDFError,
    LLMConfigurationError,
    RAGChainError,
)

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Document Intelligence System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Enterprise Aesthetic
CUSTOM_CSS = """
<style>
    /* Global Typography & Theme overrides */
    .main {
        padding-top: 1rem;
    }
    .stApp {
        background-color: #0e1117;
        color: #e0e6ed;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 198, 255, 0.3);
    }
    /* Card Component Styling */
    .info-card {
        background: linear-gradient(135deg, #1e2640 0%, #151b2e 100%);
        border: 1px solid #2e3a59;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .answer-card {
        background: linear-gradient(135deg, #132743 0%, #0b1a2e 100%);
        border-left: 5px solid #00c6ff;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }
    .citation-badge {
        display: inline-block;
        background-color: #00c6ff;
        color: #000000;
        font-weight: 700;
        border-radius: 16px;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        font-size: 0.85rem;
    }
    .chunk-box {
        background-color: #1a2235;
        border: 1px solid #2a364f;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        font-family: monospace;
        font-size: 0.9rem;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def init_session_state():
    """Initializes Streamlit session state variables."""
    if "processed_doc" not in st.session_state:
        st.session_state.processed_doc = None
    if "qa_service" not in st.session_state:
        st.session_state.qa_service = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "groq_key" not in st.session_state:
        st.session_state.groq_key = Settings.GROQ_API_KEY

def render_sidebar():
    """Renders the Streamlit sidebar for settings and document upload."""
    with st.sidebar:
        st.title("📄 Doc Intelligence")
        st.caption("Powered by LangChain, FAISS & ChatGroq")
        st.markdown("---")

        # API Key Input
        st.subheader("🔑 API Configuration")
        user_key = st.text_input(
            "Groq API Key",
            value=st.session_state.groq_key,
            type="password",
            help="Enter your Groq API key here or define GROQ_API_KEY in .env file."
        )
        if user_key:
            st.session_state.groq_key = user_key

        st.markdown("---")

        # File Upload Section
        st.subheader("📤 Document Ingestion")
        uploaded_file = st.file_uploader(
            "Upload Target PDF",
            type=["pdf"],
            help="Select any PDF document to process and index into FAISS."
        )

        # Advanced Settings Accordion
        with st.expander("⚙️ Pipeline Settings", expanded=False):
            chunk_size = st.number_input("Chunk Size", value=Settings.CHUNK_SIZE, step=100)
            chunk_overlap = st.number_input("Chunk Overlap", value=Settings.CHUNK_OVERLAP, step=25)
            retriever_k = st.number_input("Retriever Top-K", value=Settings.RETRIEVER_K, step=1)
            model_name = st.selectbox(
                "Groq Model",
                options=["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "llama-3.1-8b-instant"],
                index=0
            )

        process_button = st.button("⚡ Process Document", use_container_width=True, type="primary")

        st.markdown("---")
        st.caption("Developed following Clean Architecture & SOLID Principles.")

        return uploaded_file, process_button, chunk_size, chunk_overlap, retriever_k, model_name

def process_document_pipeline(uploaded_file, chunk_size, chunk_overlap):
    """Handles PDF ingestion progress and state updates."""
    status_box = st.empty()
    progress_bar = st.progress(0)

    try:
        status_box.info("🔍 Validating PDF file structure...")
        progress_bar.progress(20)
        time.sleep(0.3)

        pdf_bytes = uploaded_file.read()
        filename = uploaded_file.name

        status_box.info("⚙️ Initializing Document Processing Service...")
        progress_bar.progress(40)

        doc_service = DocumentProcessingService(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        status_box.info("🧠 Splitting text & generating embeddings into FAISS...")
        progress_bar.progress(70)

        result = doc_service.process_pdf(file_source=pdf_bytes, filename=filename)
        progress_bar.progress(100)

        st.session_state.processed_doc = result
        st.session_state.qa_service = None  # Reset QA service to reload with updated key/retriever

        status_box.success(
            f"✅ Document '{filename}' indexed successfully! "
            f"({'Loaded from Cache' if result['is_cached'] else 'New FAISS Index Created'})"
        )
        time.sleep(1.0)
        status_box.empty()
        progress_bar.empty()

    except (InvalidPDFError, EmptyPDFError, PDFProcessingError) as e:
        status_box.empty()
        progress_bar.empty()
        st.error(f"❌ PDF Ingestion Error: {str(e)}")
    except Exception as e:
        status_box.empty()
        progress_bar.empty()
        st.error(f"❌ Unexpected Processing Error: {str(e)}")

def render_main_area(retriever_k, model_name):
    """Renders main interface area."""
    st.header("💡 Document Intelligence & Retrieval QA")

    doc_info = st.session_state.processed_doc

    if not doc_info:
        st.info("👈 Please upload a PDF document from the sidebar and click **Process Document** to begin.")
        
        # Display Features Overview
        st.markdown("### System Architecture Features")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            #### 📄 Ingestion & Chunking
            - PyPDFLoader page extraction
            - Recursive Character Splitting
            - Configurable size & overlap
            """)
        with col2:
            st.markdown("""
            #### ⚡ FAISS Vector Store
            - Local disk caching via MD5 hashes
            - HuggingFace `all-MiniLM-L6-v2`
            - Fast similarity search retrieval
            """)
        with col3:
            st.markdown("""
            #### 🧠 ChatGroq LLM
            - LCEL RAG execution chain
            - Grounded prompt templates
            - Exact source page citations
            """)
        return

    # Document Status Banner
    st.markdown(f"""
    <div class="info-card">
        <h4 style="margin:0; color:#00c6ff;">📑 Active Document: {doc_info['filename']}</h4>
        <p style="margin:5px 0 0 0; color:#a0aec0; font-size:0.9rem;">
            <strong>Pages:</strong> {doc_info['total_pages']} | 
            <strong>Chunks:</strong> {doc_info['total_chunks']} | 
            <strong>MD5 Hash:</strong> <code>{doc_info['file_hash']}</code> | 
            <strong>Status:</strong> {'⚡ Fast Cache Load' if doc_info['is_cached'] else '🆕 Newly Vectorized'}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Question Input Form
    with st.form(key="qa_form", clear_on_submit=False):
        question = st.text_input(
            "Ask a question based on the uploaded document:",
            placeholder="e.g. What are the key requirements or findings mentioned in this document?",
            key="user_question"
        )
        submit_button = st.form_submit_button("🔍 Submit Question", type="primary")

    if submit_button and question:
        if not st.session_state.groq_key:
            st.error("⚠️ Groq API Key missing! Please enter your key in the sidebar.")
            return

        try:
            with st.spinner("🧠 Querying FAISS index & generating answer via ChatGroq..."):
                start_time = time.time()

                # Instantiate or reuse QA service
                retriever = doc_info["vectorstore"].as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": retriever_k}
                )

                qa_service = RetrievalQAService(
                    retriever=retriever,
                    api_key=st.session_state.groq_key,
                    model_name=model_name
                )

                response = qa_service.answer_question(question)
                latency = round(time.time() - start_time, 2)
                response["latency"] = latency

                # Store in history
                st.session_state.chat_history.insert(0, response)

        except LLMConfigurationError as e:
            st.error(f"🔑 LLM Configuration Error: {str(e)}")
        except RAGChainError as e:
            st.error(f"⛓️ RAG Execution Error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error generating answer: {str(e)}")

    # Render Latest or Historical Q&A Results
    if st.session_state.chat_history:
        latest = st.session_state.chat_history[0]

        st.markdown("### 🎯 Answer")
        st.markdown(f"""
        <div class="answer-card">
            <h4 style="margin-top:0; color:#00c6ff;">Q: {latest['query']}</h4>
            <div style="font-size:1.05rem; line-height:1.6;">
                {latest['answer']}
            </div>
            <div style="margin-top:1rem; font-size:0.85rem; color:#8899a6;">
                ⏱️ Latency: {latest.get('latency', 'N/A')}s
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Source Page Badges
        st.markdown("#### 📌 Cited Source Pages")
        if latest["source_pages"]:
            badges_html = " ".join(
                [f'<span class="citation-badge">Page {p}</span>' for p in latest["source_pages"]]
            )
            st.markdown(badges_html, unsafe_allow_html=True)
        else:
            st.write("No specific source pages referenced.")

        st.markdown("---")

        # Retrieved Context Chunks Expander
        with st.expander("📚 Inspect Retrieved Context Chunks", expanded=True):
            for chunk in latest["retrieved_chunks"]:
                st.markdown(f"""
                <div class="chunk-box">
                    <strong style="color:#00c6ff;">Chunk #{chunk['chunk_id']} (Page {chunk['page_number']})</strong><br/>
                    {chunk['content']}
                </div>
                """, unsafe_allow_html=True)

        # Debug Section Expander
        with st.expander("🛠️ Debug Telemetry & Raw Document Metadata", expanded=False):
            st.json({
                "query": latest["query"],
                "source_pages": latest["source_pages"],
                "total_chunks_retrieved": len(latest["retrieved_chunks"]),
                "file_hash": doc_info["file_hash"],
                "model_name": model_name,
                "retriever_k": retriever_k
            })

def main():
    """Main Streamlit Application Entrypoint."""
    init_session_state()

    (
        uploaded_file,
        process_button,
        chunk_size,
        chunk_overlap,
        retriever_k,
        model_name
    ) = render_sidebar()

    if process_button and uploaded_file is not None:
        process_document_pipeline(uploaded_file, chunk_size, chunk_overlap)

    render_main_area(retriever_k, model_name)

if __name__ == "__main__":
    main()
