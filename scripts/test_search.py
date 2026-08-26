from app.rag.retriever import RAGRetriever


def main():

    retriever = RAGRetriever()

    queries = [
        "How long do I have to return an unused backpack?",
        "Do you ship to Canada?",
        "What is the warranty period?",
    ]

    for query in queries:

        print("\n" + "=" * 70)
        print("QUERY:", query)
        print("=" * 70)

        results = retriever.search(
            query,
            n_results=5,
        )

        for i, result in enumerate(
            results,
            start=1,
        ):

            metadata = result["metadata"]

            print(
                f"\n[{i}] "
                f"{metadata.get('filename')} "
                f"| "
                f"{metadata.get('heading')}"
            )

            print(
                f"Distance: "
                f"{result['distance']:.4f}"
            )

            print(
                result["text"][:350]
            )


if __name__ == "__main__":
    main()