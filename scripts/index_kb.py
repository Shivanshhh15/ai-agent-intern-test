from app.rag.retriever import RAGRetriever


def main():
    retriever = RAGRetriever()
    retriever.build_index()


if __name__ == "__main__":
    main()