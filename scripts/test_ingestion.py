from app.pipelines.ingestion_pipeline import IngestionPipeline


def main():

    pipeline = IngestionPipeline()

    result = pipeline.ingest(
        "https://github.com/langchain-ai/langchain.git"
    )

    print(result)


if __name__ == "__main__":
    main()