from app.graph.graph_service import GraphService
from app.pipelines.graph_ingestion_pipeline import (
    GraphIngestionPipeline,
)


def main():

    graph_service = GraphService()

    graph_service.clear_database()

    pipeline = GraphIngestionPipeline()

    pipeline.ingest(
        repository_path="data/repositories/langchain.git",
        repository_name="langchain",
    )

    graph_service.close()


if __name__ == "__main__":
    main()