from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer

from app.config import CHROMA_PATH
from app.rag.chunker import chunk_markdown
from app.rag.loader import load_knowledge_base


class RAGRetriever:

    def __init__(self):
        # Free local embedding model
        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        # ChromaDB persistent storage
        self.db = chromadb.PersistentClient(
            path=CHROMA_PATH
        )

        self.collection = (
            self.db.get_or_create_collection(
                name="aster_row_kb"
            )
        )

    def build_index(
        self,
        kb_path: str = "knowledge-base",
    ):
        documents = load_knowledge_base(kb_path)

        # Exclude outdated/unapproved content
        excluded_files = {
            "02-returns-policy-legacy.md",
            "14-internal-content-migration-notes.md",
        }

        documents = [
            document
            for document in documents
            if document["metadata"].get("filename")
            not in excluded_files
        ]

        chunks = []

        for document in documents:
            document_chunks = chunk_markdown(
                document["content"],
                document["metadata"],
            )

            chunks.extend(document_chunks)

        if not chunks:
            raise RuntimeError(
                "No knowledge-base chunks found."
            )

        # Remove previous index so repeated runs
        # don't create duplicate chunks.
        existing = self.collection.get()

        if existing["ids"]:
            self.collection.delete(
                ids=existing["ids"]
            )

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        print(
            f"Creating local embeddings for "
            f"{len(texts)} chunks..."
        )

        embeddings = self.embedding_model.encode(
            texts,
            show_progress_bar=True,
            normalize_embeddings=True,
        ).tolist()

        ids = [
            f"chunk-{i}"
            for i in range(len(chunks))
        ]

        metadatas = [
            self._clean_metadata(
                chunk["metadata"]
            )
            for chunk in chunks
        ]

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print(
            f"Indexed {len(chunks)} chunks."
        )

    @staticmethod
    def _clean_metadata(
        metadata: dict[str, Any],
    ) -> dict[str, Any]:

        cleaned = {}

        for key, value in metadata.items():

            if value is None:
                continue

            if isinstance(
                value,
                (str, int, float, bool),
            ):
                cleaned[key] = value
            else:
                cleaned[key] = str(value)

        return cleaned

    def search(
        self,
        query: str,
        n_results: int = 6,
    ) -> list[dict[str, Any]]:

        query_embedding = self.embedding_model.encode(
            query,
            normalize_embeddings=True,
        ).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        output = []

        documents = results.get(
            "documents",
            [[]],
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]],
        )[0]

        distances = results.get(
            "distances",
            [[]],
        )[0]

        for i, document in enumerate(documents):

            output.append(
                {
                    "text": document,
                    "metadata": metadatas[i],
                    "distance": distances[i],
                }
            )

        return output