from app.parsing.repository_parser import RepositoryParser
from app.graph.graph_builder import GraphBuilder
from app.graph.neo4j_ingestion import Neo4jIngestionService
from app.graph.graph_service import GraphService
from app.core.logger import logger
from app.git.git_history_parser import GitHistoryParser
from app.graph.commit_graph_builder import CommitGraphBuilder


class GraphIngestionPipeline:

    def __init__(self):

        self.repository_parser = RepositoryParser()

        self.git_history_parser = GitHistoryParser()

        self.commit_graph_builder = CommitGraphBuilder()

        self.ingestion_service = Neo4jIngestionService()

        self.graph_service = GraphService()

    def ingest(
        self,
        user_id: str,
        repository_path: str,
        repository_name: str,
    ):

        graph_builder = GraphBuilder(
            repository_root=repository_path,
        )

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

        graph_data = graph_builder.build(
            parsed_repository=parsed_repository,
            user_id=user_id,
            repository_name=repository_name,
        )

        logger.info(
            "Step 3 : Parsing git history..."
        )

        commits = self.git_history_parser.parse(
            repository_path
        )

        logger.info(
            "Step 4 : Building commit graph..."
        )

        commit_graph = self.commit_graph_builder.build(
            commits=commits,
            user_id=user_id,
            repository_name=repository_name,
        )

        graph_data.merge(commit_graph)

        logger.info(
            "Step 5 : Creating Neo4j constraints..."
        )

        self.graph_service.create_constraints()

        logger.info(
            "Step 6 : Writing graph to Neo4j..."
        )

        self.ingestion_service.ingest(
            graph_data
        )

        logger.info(
            "Graph ingestion completed successfully."
        )