from src.document_loader import load_document
from src.text_splitter import split_text
from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore
from src.llm import LLM


class RAGPipeline:

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore(
            self.embedding_model
        )

        self.llm = LLM()

        self.document_content = None  # Store document content for preview

    def ingest_document(
        self,
        file_bytes: bytes,
        filename: str
    ) -> tuple[int, list[tuple[int, str]]]:

        pages = load_document(
            file_bytes,
            filename
        )

        if not pages:
            raise ValueError(
                "The uploaded document contains no readable text."
            )

        chunks = split_text(pages)

        if not chunks:
            raise ValueError(
                "Unable to create document chunks."
            )

        self.vector_store.clear()

        self.vector_store.add_documents(chunks)

        # Store document content for preview
        if pages and isinstance(pages[0], tuple):
            self.document_content = "".join(page_text for _, page_text in pages)
        else:
            self.document_content = "".join(pages) if isinstance(pages, list) else str(pages)

        return len(chunks), pages

    def get_document_preview(self, max_chars: int = 1500) -> str:
        """Get a preview of the uploaded document content."""
        if self.document_content:
            return self.document_content[:max_chars]
        return None

    def get_full_document_content(self) -> str:
        """Get the complete document content."""
        return self.document_content

    def answer_question(
        self,
        question: str,
        top_k: int = 4
    ):

        relevant_chunks = self.vector_store.search(
            question,
            top_k=top_k
        )

        answer = self.llm.generate_answer(
            question,
            relevant_chunks
        )

        return answer, relevant_chunks