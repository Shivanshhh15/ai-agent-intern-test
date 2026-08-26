from pathlib import Path

from app.rag.chunker import chunk_markdown
from app.rag.loader import load_knowledge_base


def main():

    documents = load_knowledge_base(
        Path("knowledge-base")
    )

    print(
        f"Documents loaded: {len(documents)}"
    )

    total_chunks = 0

    for document in documents:

        chunks = chunk_markdown(
            document["content"],
            document["metadata"],
        )

        total_chunks += len(chunks)

        print(
            f"{document['metadata']['filename']}: "
            f"{len(chunks)} chunks"
        )

        if chunks:
            print(
                "  First heading:",
                chunks[0]["metadata"].get(
                    "heading"
                ),
            )

    print(
        f"\nTotal chunks: {total_chunks}"
    )


if __name__ == "__main__":
    main()