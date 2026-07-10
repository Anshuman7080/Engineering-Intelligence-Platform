from app.retrieval.retriever import Retriever


def main():

    retriever = Retriever()

    results = retriever.search(
        query="what is langchain?",
        repository_name="langchain.git",
        top_k=5,
    )

    print(f"Retrieved {len(results)} results\n")

    for i, result in enumerate(results, start=1):

        print("=" * 80)
        print(f"Result {i}")
        print("=" * 80)

        print(f"Score : {result.score}")
        print(f"Source: {result.metadata['source']}")
        print()

        print(result.metadata["text"][:1000])
        print()


if __name__ == "__main__":
    main()