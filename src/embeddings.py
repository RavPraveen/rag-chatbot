from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Wrapper around the sentence-transformers embedding model.
    """
    #model selection
    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    #converting the document in to list of list with each chunk encoded
    def embed_documents(self, documents: list[str]):
        return self.model.encode(
            documents,
            normalize_embeddings=True
        ).tolist()
    #converting the user question in to a list of number
    def embed_query(self, query: str):
        return self.model.encode(
            query,
            normalize_embeddings=True
        ).tolist()