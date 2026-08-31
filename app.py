import re

import streamlit as st
from dotenv import load_dotenv

from src.rag_pipeline import RAGPipeline


load_dotenv()


st.set_page_config(
    page_title="Document Q&A",
    page_icon="📚",
    layout="wide"
)


@st.cache_resource
def create_pipeline():
    return RAGPipeline()


pipeline = create_pipeline()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📚 Document Q&A Assistant")

st.write(
    "Upload a PDF or text document and ask questions "
    "about its content."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("Document")

    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["pdf", "txt"]
    )

    if uploaded_file:

        if st.button(
            "Process Document",
            use_container_width=True
        ):

            with st.spinner("Processing document..."):

                try:

                    number_of_chunks = (
                        pipeline.ingest_document(
                            uploaded_file.getvalue(),
                            uploaded_file.name
                        )
                    )

                    st.session_state.document_processed = True
                    st.session_state.document_name = uploaded_file.name
                    st.session_state.chunk_count = number_of_chunks

                    st.success(
                        f"Processed {number_of_chunks} chunks."
                    )

                except Exception as error:

                    st.error(str(error))


    if st.session_state.get("document_processed"):

        st.divider()

        st.success(
            f"Loaded: {st.session_state.document_name}"
        )

        st.caption(
            f"Document chunks: "
            f"{st.session_state.chunk_count}"
        )


# --------------------------------------------------
# Question input
# --------------------------------------------------

if not st.session_state.get("document_processed"):

    st.info(
        "Upload a document and click "
        "'Process Document' to begin."
    )

else:

    st.subheader("Ask a question")

    question = st.text_input(
        "Question",
        placeholder="Ask something about the document..."
    )

    if st.button(
        "Get Answer",
        type="primary"
    ):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner("Searching document..."):

                try:

                    answer, sources = (
                        pipeline.answer_question(
                            question
                        )
                    )

                    st.subheader("Answer")

                    st.write(answer)

                    with st.expander(
                        "View retrieved context"
                    ):

                        for i, source in enumerate(
                            sources,
                            start=1
                        ):

                            match = re.search(
                                r"\[Page\s+(\d+)\]",
                                source
                            )
                            page_number = (
                                match.group(1)
                                if match
                                else "Unknown"
                            )

                            st.markdown(
                                f"**Source {i}**"
                            )
                            st.caption(
                                f"Page {page_number}"
                            )
                            st.write(source)

                except Exception as error:

                    st.error(
                        f"Unable to generate answer: {error}"
                    )