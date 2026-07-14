from app.parsing.repository_parser import RepositoryParser
from app.graph.graph_builder import GraphBuilder
from app.graph.neo4j_ingestion import Neo4jIngestionService
from app.core.logger import logger


class GraphIngestionPipeline:

    def __init__(self):

        self.repository_parser = RepositoryParser()

        self.graph_builder = GraphBuilder()

        self.ingestion_service = Neo4jIngestionService()

    def ingest(
        self,
        repository_path: str,
        repository_name: str,
    ):

        logger.info(
            "Step 1 : Parsing repository..."
        )

        parsed_repository = (
            self.repository_parser.parse_repository(
                repository_path
            )
        )

        logger.info(
            "Step 2 : Building graph..."
        )

        graph_data = self.graph_builder.build(
            parsed_repository=parsed_repository,
            repository_name=repository_name,
        )

        logger.info(
            "Step 3 : Writing graph to Neo4j..."
        )

        self.ingestion_service.ingest(
            graph_data
        )

        logger.info(
            "Graph ingestion completed successfully."
        )