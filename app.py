import streamlit as st
from dotenv import load_dotenv

from src.rag_pipeline import RAGPipeline

load_dotenv()

# ---------------------------------------------
# Page Configuration
# ---------------------------------------------
st.set_page_config(
    page_title="DocuMind — AI Document Assistant",
    page_icon="🧠",
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
    .main .block-container {
        padding: 2rem 2.5rem 3rem 2.5rem;
        max-width: 960px;
    }

    /* ===== Scrollbar ===== */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.18); }

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
        padding: 2.5rem 1rem 1rem 1rem;
        margin-bottom: 0.5rem;
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

    /* ===== Feature Cards (Empty State) ===== */
    .feature-card {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all var(--transition-smooth);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--gradient-primary);
        opacity: 0;
        transition: opacity var(--transition-smooth);
    }
    .feature-card:hover {
        border-color: var(--border-accent);
        transform: translateY(-4px);
        box-shadow: var(--shadow-md), var(--shadow-glow);
    }
    .feature-card:hover::before {
        opacity: 1;
    }
    .feature-icon {
        font-size: 2.2rem;
        margin-bottom: 0.8rem;
        display: block;
    }
    .feature-title {
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        font-size: 0.85rem;
        color: var(--text-secondary);
        line-height: 1.55;
    }

    /* ===== Empty State Banner ===== */
    .empty-banner {
        background: var(--gradient-card);
        border: 1px dashed rgba(99, 102, 241, 0.25);
        border-radius: var(--radius-lg);
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0 2rem 0;
    }
    .empty-banner-icon {
        font-size: 2.8rem;
        margin-bottom: 0.6rem;
        display: block;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    .empty-banner-text {
        font-size: 1rem;
        color: var(--text-secondary);
        font-weight: 400;
    }
    .empty-banner-text strong {
        color: var(--accent-indigo);
    }

    /* ===== Chat Messages ===== */
    .stChatMessage {
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border-subtle) !important;
        margin-bottom: 1rem !important;
        padding: 1rem 1.2rem !important;
        background: var(--bg-glass) !important;
        backdrop-filter: blur(6px) !important;
        transition: var(--transition-fast);
    }
    .stChatMessage:hover {
        border-color: var(--border-accent) !important;
    }

    /* ===== Chat Input ===== */
    .stChatInput > div {
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border-subtle) !important;
        background: var(--bg-glass) !important;
        backdrop-filter: blur(6px) !important;
        transition: var(--transition-smooth);
    }
    .stChatInput > div:focus-within {
        border-color: var(--accent-indigo) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12) !important;
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


# ---------------------------------------------
# Sidebar Interface
# ---------------------------------------------
with st.sidebar:
    # Branding
    st.markdown("""
        <div class="sidebar-brand">
            <span class="sidebar-brand-icon">🧠</span>
            <div>
                <div class="sidebar-brand-text">DocuMind</div>
                <div class="sidebar-brand-sub">AI Document Assistant</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Upload Section
    st.markdown('<div class="sidebar-section-header">📁 Document Upload</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Source File",
        type=["pdf", "txt"],
        help="Supported formats: PDF, TXT",
        label_visibility="collapsed"
    )

    if uploaded_file:
        process_button = st.button(
            "⚡ Process & Index Document",
            use_container_width=True,
            type="primary"
        )

        if process_button:
            with st.spinner("Analyzing and indexing document..."):
                try:
                    number_of_chunks = pipeline.ingest_document(
                        uploaded_file.getvalue(),
                        uploaded_file.name
                    )

                    st.session_state.document_processed = True
                    st.session_state.document_name = uploaded_file.name
                    st.session_state.chunk_count = number_of_chunks
                    st.session_state.messages = []  # Reset chat on new file upload

                    st.success("✅ Document indexed successfully!")

                except Exception as error:
                    st.error(f"Failed to process document: {error}")

    st.divider()

    # Document Status
    st.markdown('<div class="sidebar-section-header">📊 Document Status</div>', unsafe_allow_html=True)

    if st.session_state.document_processed:
        st.markdown(
            '<span class="badge badge-active"><span class="pulse-dot"></span> Active</span>',
            unsafe_allow_html=True
        )

        st.markdown(f"""
            <div class="status-card">
                <div class="metric-row">
                    <span class="metric-icon">📄</span>
                    <span class="metric-label">File</span>
                    <span class="metric-value">{st.session_state.document_name}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-icon">🧩</span>
                    <span class="metric-label">Chunks</span>
                    <span class="metric-value">{st.session_state.chunk_count}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-icon">💬</span>
                    <span class="metric-label">Messages</span>
                    <span class="metric-value">{len(st.session_state.messages)}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("🗑️ Clear Chat History", use_container_width=True):
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

# Empty State
if not st.session_state.document_processed:
    st.markdown("""
        <div class="empty-banner">
            <span class="empty-banner-icon">📂</span>
            <div class="empty-banner-text">
                Upload a <strong>PDF</strong> or <strong>TXT</strong> file from the sidebar to get started.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Feature Highlights Grid
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown("""
            <div class="feature-card">
                <span class="feature-icon">📄</span>
                <div class="feature-title">Multi-Format Support</div>
                <div class="feature-desc">Upload text files or PDF documents seamlessly for instant indexing.</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="feature-card">
                <span class="feature-icon">🎯</span>
                <div class="feature-title">Context-Aware Answers</div>
                <div class="feature-desc">Responses are sourced directly from your uploaded content with RAG.</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="feature-card">
                <span class="feature-icon">🔍</span>
                <div class="feature-title">Full Transparency</div>
                <div class="feature-desc">Inspect the exact document chunks used for every generated response.</div>
            </div>
        """, unsafe_allow_html=True)

else:
    # Render Existing Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Render retrieved context chunks for assistant messages
            if message["role"] == "assistant" and "chunks" in message:
                chunks = message.get("chunks", [])
                if chunks:
                    with st.expander("🔍 View Retrieved Context", expanded=False):
                        for i, chunk in enumerate(chunks, start=1):
                            st.markdown(
                                f'<div class="chunk-card"><div class="chunk-label">Source Chunk {i}</div>{chunk}</div>',
                                unsafe_allow_html=True
                            )

    # Chat Input Handling
    if question := st.chat_input("Ask a question about your document..."):
        # Store & Display User Message
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Generate & Display Assistant Response
        with st.chat_message("assistant"):
            with st.spinner("Searching document context..."):
                try:
                    answer, chunks = pipeline.answer_question(question)

                    st.markdown(answer)

                    if chunks:
                        with st.expander("🔍 View Retrieved Context", expanded=False):
                            for i, chunk in enumerate(chunks, start=1):
                                st.markdown(
                                    f'<div class="chunk-card"><div class="chunk-label">Source Chunk {i}</div>{chunk}</div>',
                                    unsafe_allow_html=True
                                )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "chunks": chunks
                    })

                except Exception as error:
                    error_message = f"An error occurred while generating the response: {error}"
                    st.error(error_message)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message,
                        "chunks": []
                    })