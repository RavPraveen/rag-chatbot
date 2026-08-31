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


# ---------------------------------------------
# Session state
# ---------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_processed" not in st.session_state:
    st.session_state.document_processed = False


# ---------------------------------------------
# Sidebar
# ---------------------------------------------

with st.sidebar:

    st.header("📄 Document")

    uploaded_file = st.file_uploader(
        "Upload PDF or TXT",
        type=["pdf", "txt"]
    )

    if uploaded_file:

        if st.button(
            "Process Document",
            use_container_width=True
        ):

            with st.spinner("Processing document..."):

                try:

                    number_of_chunks = pipeline.ingest_document(
                        uploaded_file.getvalue(),
                        uploaded_file.name
                    )

                    st.session_state.document_processed = True
                    st.session_state.document_name = uploaded_file.name
                    st.session_state.chunk_count = number_of_chunks

                    # Clear old conversation when a new document
                    # is uploaded
                    st.session_state.messages = []

                    st.success(
                        f"Processed {number_of_chunks} chunks."
                    )

                except Exception as error:

                    st.error(str(error))


# ---------------------------------------------
# Main interface
# ---------------------------------------------

st.title("📚 Document Q&A Assistant")

st.caption(
    "Ask questions about your uploaded document."
)


if not st.session_state.document_processed:

    st.info(
        "Upload a document and process it to start chatting."
    )

else:

    # -----------------------------------------
    # Display previous messages
    # -----------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            # Show retrieved chunks for assistant messages
            if message["role"] == "assistant":

                chunks = message.get("chunks", [])

                with st.expander(
                    "🔍 View retrieved context"
                ):

                    if chunks:

                        for i, chunk in enumerate(
                            chunks,
                            start=1
                        ):

                            st.markdown(
                                f"**Chunk {i}**"
                            )

                            st.write(chunk)

                            if i < len(chunks):
                                st.divider()

                    else:

                        st.write(
                            "No relevant chunks were retrieved."
                        )


    # -----------------------------------------
    # New question
    # -----------------------------------------

    question = st.chat_input(
        "Ask a question..."
    )


    if question:

        # -----------------------------------------
        # User message
        # -----------------------------------------

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):

            st.markdown(question)


        # -----------------------------------------
        # Generate answer
        # -----------------------------------------

        with st.chat_message("assistant"):

            with st.spinner("Searching document..."):

                try:

                    answer, chunks = pipeline.answer_question(
                        question
                    )

                    st.markdown(answer)

                    # ---------------------------------
                    # Retrieved context
                    # ---------------------------------

                    with st.expander(
                        "🔍 View retrieved context"
                    ):

                        if chunks:

                            for i, chunk in enumerate(
                                chunks,
                                start=1
                            ):

                                st.markdown(
                                    f"**Chunk {i}**"
                                )

                                st.write(chunk)

                                if i < len(chunks):
                                    st.divider()

                        else:

                            st.write(
                                "No relevant chunks were retrieved."
                            )


                except Exception as error:

                    answer = (
                        "Sorry, I couldn't process "
                        "your question."
                    )

                    chunks = []

                    st.error(str(error))


        # -----------------------------------------
        # Store assistant response + chunks
        # -----------------------------------------

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "chunks": chunks
        })