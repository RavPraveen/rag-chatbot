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

        return len(chunks), pages

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