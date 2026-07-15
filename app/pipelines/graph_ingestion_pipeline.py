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

        self.graph_service=GraphService()

    def ingest(
        self,
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
            repository_name=repository_name,
        )

        logger.info(
            "step3 : parsing git commits"
        )

        commits = self.git_history_parser.parse(
            repository_path
        )

        commit_graph = self.commit_graph_builder.build(
            commits=commits,
            repository_name=repository_name,
        )

        graph_data.merge(commit_graph)

        logger.info(
            "Step 4 : Writing graph to Neo4j..."
        )

        self.graph_service.create_constraints()

        modify_count = sum(
            1
            for r in graph_data.relationships
            if r.relationship == "MODIFIES"
        )

        print(f"MODIFIES relationships: {modify_count}")

        commit_count = sum(
            1
            for n in graph_data.nodes
            if n.label == "Commit"
        )

        print(f"Commit nodes: {commit_count}")


        self.ingestion_service.ingest(
            graph_data
        )

        logger.info(
            "Graph ingestion completed successfully."
        )