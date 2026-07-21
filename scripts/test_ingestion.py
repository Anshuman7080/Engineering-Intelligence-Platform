from app.pipelines.ingestion_service import IngestionService


def main():

    service = IngestionService()

    result = service.ingest(
        repository_url="https://github.com/langchain-ai/langchain"
    )

    print("\n========== INGESTION RESULT ==========\n")
    print(result)


if __name__ == "__main__":
    main()