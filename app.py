import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

from src.rag_pipeline import RAGPipeline

load_dotenv()

# ---------------------------------------------
# Page Configuration
# ---------------------------------------------
st.set_page_config(
    page_title="DocuBot — AI Document Assistant",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------
# Custom Styling (CSS) — Professional Dark Theme
# ---------------------------------------------
st.markdown("""
<style>
    /* ===== Google Fonts ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    /* ===== Root Variables ===== */
    :root {
        --bg-primary: #0f1117;
        --bg-secondary: #161b22;
        --bg-card: rgba(22, 27, 34, 0.7);
        --bg-glass: rgba(255, 255, 255, 0.03);
        --border-subtle: rgba(255, 255, 255, 0.06);
        --border-accent: rgba(99, 102, 241, 0.3);
        --text-primary: #e6edf3;
        --text-secondary: #8b949e;
        --text-muted: #6e7681;
        --accent-indigo: #6366f1;
        --accent-violet: #8b5cf6;
        --accent-emerald: #10b981;
        --accent-rose: #f43f5e;
        --accent-amber: #f59e0b;
        --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a78bfa 100%);
        --gradient-card: linear-gradient(135deg, rgba(99,102,241,0.08) 0%, rgba(139,92,246,0.05) 100%);
        --gradient-sidebar: linear-gradient(180deg, rgba(99,102,241,0.06) 0%, transparent 40%);
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
        --shadow-md: 0 4px 16px rgba(0,0,0,0.4);
        --shadow-lg: 0 8px 32px rgba(0,0,0,0.5);
        --shadow-glow: 0 0 20px rgba(99,102,241,0.15);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --transition-fast: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-smooth: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    /* ===== Global Reset ===== */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary);
    }
    /* ===== Main Container ===== */
    .main {
        overflow: hidden !important;
    }
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        height: calc(100vh - 150px);
        display: flex;
        flex-direction: column;
    }
    
    /* Hero container takes fixed space */
    .main .block-container > .element-container:first-child {
        flex-shrink: 0;
    }
    
    /* Main content below hero */
    .main .block-container > .element-container:nth-child(2) {
        flex: 1;
        min-height: 0;
        overflow: hidden;
        padding: 1.5rem 2.5rem !important;
    }
    /* Keep the columns fixed. The document viewer and chat area
       manage their own scrolling independently. */
    [data-testid="stColumn"] {
        overflow: hidden !important;
    }
    /* Fixed-height Streamlit containers can scroll internally. */
    [data-testid="stVerticalBlockBorderWrapper"] {
        min-height: 0;
    }
    /* ===== Scrollbar ===== */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.18); }
    
    /* Disable main page scrolling */
    html, body {
        overflow: hidden !important;
        height: 100vh !important;
    }
    
   
    /* ===== Sidebar ===== */
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-subtle) !important;
    }
    section[data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 200px;
        background: var(--gradient-sidebar);
        pointer-events: none;
        z-index: 0;
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }
    /* ===== Hero Title ===== */
    .hero-container {
        text-align: center;
        padding: 2rem 2.5rem 1.5rem 2.5rem;
        margin: 0;
        border-bottom: 1px solid var(--border-subtle);
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: var(--text-secondary);
        font-weight: 400;
        max-width: 520px;
        margin: 0 auto;
        line-height: 1.6;
    }
    /* ===== Sidebar Branding ===== */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0 0 0.8rem 0;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid var(--border-subtle);
    }
    .sidebar-brand-icon {
        font-size: 1.7rem;
        line-height: 1;
    }
    .sidebar-brand-text {
        font-size: 1.2rem;
        font-weight: 700;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sidebar-brand-sub {
        font-size: 0.75rem;
        color: var(--text-muted);
        font-weight: 400;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    /* ===== Status Card ===== */
    .status-card {
        background: var(--gradient-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 1rem 1.1rem;
        margin: 0.8rem 0;
        backdrop-filter: blur(8px);
        transition: var(--transition-smooth);
    }
    .status-card:hover {
        border-color: var(--border-accent);
        box-shadow: var(--shadow-glow);
    }
    .status-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
    }
    .status-value {
        font-size: 0.92rem;
        font-weight: 500;
        color: var(--text-primary);
        word-break: break-all;
    }
    /* ===== Badges ===== */
    .badge {
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        letter-spacing: 0.02em;
    }
    .badge-active {
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    .badge-inactive {
        background: rgba(244, 63, 94, 0.1);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.15);
    }
    /* (empty state cards removed — clean main area) */
    /* ===== Chat Messages ===== */
.stChatMessage {
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-subtle) !important;
    margin-bottom: 1rem !important;
    padding: 1rem 1.2rem !important;
    background: var(--bg-glass) !important;
    backdrop-filter: blur(6px) !important;
}
    .stChatMessage:hover {
        border-color: var(--border-accent) !important;
    }
    
   /* Chat input */
.stChatInput {
    flex-shrink: 0 !important;
    margin-top: 0.7rem !important;
}
.stChatInput > div {
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-subtle) !important;
    background: var(--bg-glass) !important;
}
.stChatInput > div:focus-within {
    border-color: var(--accent-indigo) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12) !important;
}
    /* ===== Disabled/Locked Chat Input Overlay ===== */
    .chat-locked-wrapper {
        position: relative;
    }
    .chat-locked-wrapper .stChatInput > div {
        opacity: 0.35 !important;
        pointer-events: none !important;
        filter: grayscale(0.5);
    }
    .chat-locked-hint {
        text-align: center;
        padding: 0.6rem 0 0.2rem 0;
        font-size: 0.82rem;
        color: var(--text-muted);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }
    .chat-locked-hint .lock-icon {
        font-size: 0.9rem;
        opacity: 0.7;
    }
    /* ===== Buttons ===== */
    .stButton > button {
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 0.55rem 1.2rem !important;
        transition: all var(--transition-smooth) !important;
        letter-spacing: 0.01em;
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background: var(--gradient-primary) !important;
        border: none !important;
        color: white !important;
        box-shadow: var(--shadow-sm) !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        box-shadow: var(--shadow-md), 0 0 24px rgba(99,102,241,0.3) !important;
        transform: translateY(-1px);
    }
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="stBaseButton-secondary"] {
        background: var(--bg-glass) !important;
        border: 1px solid var(--border-subtle) !important;
        color: var(--text-secondary) !important;
    }
    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="stBaseButton-secondary"]:hover {
        border-color: var(--border-accent) !important;
        color: var(--text-primary) !important;
        background: rgba(99,102,241,0.06) !important;
    }
    /* ===== File Uploader ===== */
    section[data-testid="stFileUploader"] {
        border-radius: var(--radius-md) !important;
    }
    section[data-testid="stFileUploader"] > div {
        border-radius: var(--radius-md) !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background: var(--bg-glass) !important;
        border: 2px dashed rgba(99, 102, 241, 0.2) !important;
        border-radius: var(--radius-md) !important;
        transition: all var(--transition-smooth);
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: rgba(99, 102, 241, 0.45) !important;
        background: rgba(99, 102, 241, 0.04) !important;
    }
    /* ===== Expander (Context Viewer) ===== */
    .streamlit-expanderHeader {
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        color: var(--text-secondary) !important;
        background: transparent !important;
        border-radius: var(--radius-sm) !important;
    }
    .streamlit-expanderContent {
        border-color: var(--border-subtle) !important;
    }
    /* ===== Dividers ===== */
    hr {
        border-color: var(--border-subtle) !important;
        opacity: 0.5;
    }
    /* ===== Info/Success/Error Alerts ===== */
    .stAlert {
        border-radius: var(--radius-sm) !important;
        font-size: 0.9rem !important;
    }
    /* ===== Sidebar Section Headers ===== */
    .sidebar-section-header {
        font-size: 0.72rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 1.2rem 0 0.5rem 0;
    }
    /* ===== Metric Pill ===== */
    .metric-row {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 0.35rem 0;
    }
    .metric-icon {
        font-size: 0.9rem;
        width: 20px;
        text-align: center;
    }
    .metric-label {
        font-size: 0.82rem;
        color: var(--text-secondary);
        flex: 1;
    }
    .metric-value {
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--text-primary);
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
    }
    /* ===== Pulse animation for active indicator ===== */
    .pulse-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--accent-emerald);
        animation: pulse 2s ease-in-out infinite;
        vertical-align: middle;
        margin-right: 2px;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
        50% { opacity: 0.7; box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
    }
    /* ===== Chunk source card styling ===== */
    .chunk-card {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-left: 3px solid var(--accent-indigo);
        border-radius: var(--radius-sm);
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        font-size: 0.88rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    .chunk-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: var(--accent-violet);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.4rem;
    }
    /* ===== Draggable Split Resizer (Overleaf-style) ===== */
    .docmind-resizer {
        flex: 0 0 6px;
        width: 6px;
        min-width: 6px;
        cursor: col-resize;
        background: rgba(139, 92, 246, 0.35);
        border-radius: 3px;
        align-self: stretch;
        margin: 0 4px;
        position: relative;
        transition: background var(--transition-fast), box-shadow var(--transition-fast);
        z-index: 5;
        box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.04);
    }
    .docmind-resizer:hover,
    .docmind-resizer.docmind-resizing {
        background: var(--accent-indigo);
        box-shadow: var(--shadow-glow);
    }
    .docmind-resizer::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 3px;
        height: 40px;
        border-radius: 2px;
        background: rgba(255, 255, 255, 0.55);
    }
    .docmind-resizer:hover::after,
    .docmind-resizer.docmind-resizing::after {
        background: rgba(255, 255, 255, 0.9);
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------
# Pipeline Initialization
# ---------------------------------------------
@st.cache_resource
def create_pipeline():
    return RAGPipeline()

pipeline = create_pipeline()

# ---------------------------------------------
# Session State Initialization
# ---------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_processed" not in st.session_state:
    st.session_state.document_processed = False

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

if "document_bytes" not in st.session_state:
    st.session_state.document_bytes = None

if "document_type" not in st.session_state:
    st.session_state.document_type = None


# ---------------------------------------------
# Sidebar Interface
# ---------------------------------------------
with st.sidebar:
    # Branding
    st.markdown("""
        <div class="sidebar-brand">
            <span class="sidebar-brand-icon"></span>
            <div>
                <div class="sidebar-brand-text">DocuBot</div>
                <div class="sidebar-brand-sub">AI Document Assistant</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Upload Section
    st.markdown('<div class="sidebar-section-header"> Document Upload</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Source File",
        type=["pdf", "txt"],
        help="Supported formats: PDF, TXT",
        label_visibility="collapsed"
    )

    if uploaded_file:
        process_button = st.button(
            "Upload",
            use_container_width=True,
            type="primary"
        )

        if process_button:
            with st.spinner("Analyzing and indexing document..."):
                try:
                    file_bytes = uploaded_file.getvalue()
                    number_of_chunks = pipeline.ingest_document(
                        file_bytes,
                        uploaded_file.name
                    )

                    st.session_state.document_processed = True
                    st.session_state.document_name = uploaded_file.name
                    st.session_state.document_type = uploaded_file.name.lower().rsplit(".", 1)[-1] if "." in uploaded_file.name else ""
                    st.session_state.chunk_count = number_of_chunks
                    st.session_state.document_bytes = file_bytes
                    st.session_state.messages = []  # Reset chat on new file upload



                except Exception as error:
                    st.error(f"Failed to process document: {error}")

    st.divider()




    # Document Status
    st.markdown('<div class="sidebar-section-header"> Document Status</div>', unsafe_allow_html=True)

    if st.session_state.document_processed:


        st.markdown(f""" 
        <div class="status-card"> 
        <div class="metric-row"> 
            <span class="metric-icon"></span> 
            <span class="metric-label">File</span> 
            <span class="metric-value">{st.session_state.document_name}</span> 
        </div> 
         </div> 
        """, unsafe_allow_html=True)

        if st.button(" Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    else:
        st.markdown(
            '<span class="badge badge-inactive">○ No Active Document</span>',
            unsafe_allow_html=True
        )
        st.caption("Upload and process a file to begin.")

    # Footer
    st.divider()
    st.markdown("""
        <div style="text-align:center; padding: 0.5rem 0;">
            <span style="font-size: 0.72rem; color: var(--text-muted);">
                Powered by RAG · Built with Streamlit
            </span>
        </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------
# Main Application Interface
# ---------------------------------------------

# Hero Header
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Chat with Your Document</div>
        <div class="hero-subtitle">
            Extract precise insights, summaries, and answers from your files — powered by retrieval-augmented generation.
        </div>
    </div>
""", unsafe_allow_html=True)


# Two-Column Layout: Document Viewer (Left) + Chat (Right)
if st.session_state.document_processed:
    col_doc, col_chat = st.columns([0.45, 0.55], gap="medium")

    # ===== LEFT COLUMN: DOCUMENT VIEWER =====
    with col_doc:
        st.markdown("""
            <div id="docmind-viewer-marker"></div>
            <div style="margin-bottom: 1rem;">
                <h3 style="
                    font-size: 1.1rem;
                    margin: 0;
                    color: var(--text-primary);
                ">
                     Document Viewer
                </h3>
            </div>
        """, unsafe_allow_html=True)

        try:
            if st.session_state.document_bytes:
                document_type = (st.session_state.document_type or "").lower()

                if document_type == "pdf":
                    import base64

                    pdf_base64 = base64.b64encode(
                        st.session_state.document_bytes
                    ).decode("utf-8")

                    pdf_display = f"""
                        <iframe
                            src="data:application/pdf;base64,{pdf_base64}"
                            width="100%"
                            height="650"
                            type="application/pdf"
                            style="
                                border-radius: 8px;
                                border: 1px solid var(--border-subtle);
                            ">
                        </iframe>
                    """

                    st.markdown(
                        pdf_display,
                        unsafe_allow_html=True
                    )

                else:
                    preview_text = pipeline.get_full_document_content()

                    if not preview_text and st.session_state.document_bytes is not None:
                        try:
                            preview_text = st.session_state.document_bytes.decode("utf-8-sig")
                        except UnicodeDecodeError:
                            preview_text = st.session_state.document_bytes.decode("latin-1", errors="replace")

                    if not preview_text:
                        preview_text = "No text content was found in this file."

                    document_container = st.container(
                        height=650,
                        border=False
                    )

                    with document_container:
                        st.code(preview_text, language="text")

        except Exception as e:
            st.warning(f"Could not display document preview: {str(e)}")

            try:
                full_content = pipeline.get_full_document_content()

                if full_content:
                    document_container = st.container(
                        height=600,
                        border=False
                    )

                    with document_container:
                        st.text(full_content)

            except Exception:
                st.error("Document preview not available")

    # ===== RIGHT COLUMN: CHAT INTERFACE =====
    with col_chat:
        st.markdown("""
            <div style="margin-bottom: 1rem;">
                <h3 style="
                    font-size: 1.1rem;
                    margin: 0;
                    color: var(--text-primary);
                ">
                     Chat
                </h3>
            </div>
        """, unsafe_allow_html=True)

        # Scrollable message area.
        # The chat input is outside this container so it stays at the bottom.
        chat_container = st.container(
            height=555,
            border=False
        )

        with chat_container:
            if not st.session_state.messages:
                st.markdown(
                    """
                    <div style="
                        min-height: 420px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        text-align: center;
                        color: var(--text-muted);
                        font-size: 0.9rem;
                    ">
                        Ask something about your document to begin.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

                    if (
                        message["role"] == "assistant"
                        and "chunks" in message
                    ):
                        chunks = message.get("chunks", [])

                        if chunks:
                            with st.expander(
                                "🔍 View Retrieved Context",
                                expanded=False
                            ):
                                for i, chunk in enumerate(
                                    chunks,
                                    start=1
                                ):
                                    st.markdown(
                                        f"""
                                        <div class="chunk-card">
                                            <div class="chunk-label">
                                                Source Chunk {i}
                                            </div>
                                            {chunk}
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )

        # Chat input stays below the independently scrollable chat history.
        question = st.chat_input(
            "Ask a question about your document...",
            key="document_chat_input"
        )

        if question:
            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            try:
                with st.spinner("Searching document context..."):
                    answer, chunks = pipeline.answer_question(question)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "chunks": chunks
                })

            except Exception as error:
                error_message = (
                    "An error occurred while generating "
                    f"the response: {error}"
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message,
                    "chunks": []
                })

            st.rerun()

    # ---------------------------------------------
    # Draggable resizer between the two main columns
    # (Overleaf-style code/preview split)
    # ---------------------------------------------
    components.html(
        """
        <script>
        (function() {
            const doc = window.parent.document;
            const RESIZER_WIDTH = 6;
            const MIN_PCT = 20;
            const MAX_PCT = 80;
            function applySplit(leftCol, rightCol, containerWidth, leftPct) {
                const rightPct = 100 - leftPct;
                leftCol.style.flex = `0 0 ${leftPct}%`;
                leftCol.style.width = `${leftPct}%`;
                leftCol.style.maxWidth = 'none';
                rightCol.style.flex = `0 0 ${rightPct}%`;
                rightCol.style.width = `${rightPct}%`;
                rightCol.style.maxWidth = 'none';
            }
            function init() {
                const marker = doc.getElementById('docmind-viewer-marker');
                if (!marker) { setTimeout(init, 200); return; }
                const leftCol = marker.closest('[data-testid="stColumn"]');
                if (!leftCol) { setTimeout(init, 200); return; }
                const horizontalBlock = leftCol.parentElement;
                if (!horizontalBlock) { setTimeout(init, 200); return; }
                const columns = horizontalBlock.querySelectorAll(':scope > [data-testid="stColumn"]');
                if (columns.length < 2) { setTimeout(init, 200); return; }
                const rightCol = columns[1];
                horizontalBlock.style.position = 'relative';
                horizontalBlock.style.flexWrap = 'nowrap';
                horizontalBlock.style.alignItems = 'stretch';
                // Streamlit rebuilds these columns from scratch on every
                // rerun, so re-apply whatever split the user last dragged to.
                if (typeof window.__docmindSplitPct === 'number') {
                    applySplit(leftCol, rightCol, horizontalBlock.getBoundingClientRect().width, window.__docmindSplitPct);
                }
                if (horizontalBlock.querySelector('.docmind-resizer')) { return; }
                const resizer = doc.createElement('div');
                resizer.className = 'docmind-resizer';
                resizer.title = 'Drag to resize · double-click to reset';
                horizontalBlock.insertBefore(resizer, rightCol);
                let dragging = false;
                let startX = 0, startLeftPct = 0, containerWidth = 0;
                function onMouseDown(e) {
                    dragging = true;
                    startX = e.clientX;
                    containerWidth = horizontalBlock.getBoundingClientRect().width;
                    startLeftPct = (leftCol.getBoundingClientRect().width / containerWidth) * 100;
                    resizer.classList.add('docmind-resizing');
                    doc.body.style.userSelect = 'none';
                    doc.body.style.cursor = 'col-resize';
                    e.preventDefault();
                }
                function onMouseMove(e) {
                    if (!dragging) return;
                    const dxPct = ((e.clientX - startX) / containerWidth) * 100;
                    let leftPct = startLeftPct + dxPct;
                    leftPct = Math.min(MAX_PCT, Math.max(MIN_PCT, leftPct));
                    window.__docmindSplitPct = leftPct;
                    applySplit(leftCol, rightCol, containerWidth, leftPct);
                }
                function onMouseUp() {
                    if (!dragging) return;
                    dragging = false;
                    resizer.classList.remove('docmind-resizing');
                    doc.body.style.userSelect = '';
                    doc.body.style.cursor = '';
                }
                function onDoubleClick() {
                    window.__docmindSplitPct = 45;
                    applySplit(leftCol, rightCol, horizontalBlock.getBoundingClientRect().width, 45);
                }
                resizer.addEventListener('mousedown', onMouseDown);
                resizer.addEventListener('dblclick', onDoubleClick);
                // Clean up listeners from any previous rerun before adding new ones.
                if (window.__docmindCleanup) { window.__docmindCleanup(); }
                doc.addEventListener('mousemove', onMouseMove);
                doc.addEventListener('mouseup', onMouseUp);
                window.__docmindCleanup = function() {
                    doc.removeEventListener('mousemove', onMouseMove);
                    doc.removeEventListener('mouseup', onMouseUp);
                };
            }
            init();
        })();
        </script>
        """,
        height=0,
        width=0,
    )

else:
    st.markdown(
        """
        <div class="chat-locked-hint">
            <span class="lock-icon"></span>
            Upload and process a document from the sidebar to start chatting.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="chat-locked-wrapper">',
        unsafe_allow_html=True
    )

    st.chat_input(
        "Ask a question about your document...",
        disabled=True,
        key="locked_chat_input"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )
