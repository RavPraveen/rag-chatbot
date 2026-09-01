import chromadb


class VectorStore:

    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

        self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    def add_documents(self, chunks: list[str]):
        """
        Add document chunks and their embeddings to ChromaDB.
        """

        embeddings = self.embedding_model.embed_documents(chunks)

        ids = [
            f"chunk_{i}"
            for i in range(len(chunks))
        ]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings
        )
    #Searching for the most matched four chunks done by Chromadb
    def search(self, query: str, top_k: int = 4):
        """
        Retrieve the most relevant document chunks.
        """

        query_embedding = self.embedding_model.embed_query(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results["documents"][0]

    def clear(self):
        """
        Remove all stored documents.
        """

        self.client.delete_collection("documents")

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )