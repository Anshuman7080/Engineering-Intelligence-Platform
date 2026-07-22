from neo4j import GraphDatabase

from app.core.settings import settings
from app.core.logger import logger


class GraphService:

    def __init__(self):

        logger.info("Connecting to Neo4j...")
        print(settings.NEO4J_URI)

        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(
                settings.NEO4J_USERNAME,
                settings.NEO4J_PASSWORD,
            ),
        )

        logger.info("Neo4j connected successfully.")

    def close(self):
        self.driver.close()

    def execute(
        self,
        query: str,
        parameters: dict | None = None,
    ):

        with self.driver.session() as session:

            result = session.run(
                query,
                parameters or {},
            )

            return list(result)

    def execute_write(
        self,
        query: str,
        parameters: dict | None = None,
    ):

        with self.driver.session() as session:

            session.run(
                query,
                parameters or {},
            )

    def create_constraints(self):

        labels = [
            "Repository",
            "File",
            "Module",
            "Class",
            "Function",
            "Method",
        ]

        for label in labels:

            query = f"""
            CREATE CONSTRAINT IF NOT EXISTS
            FOR (n:{label})
            REQUIRE n.id IS UNIQUE
            """

            self.execute_write(query)

    def delete_repository(
        self,
        user_id: str,
        repository_name: str,
    ):

        query = """
        MATCH (n)
        WHERE
            n.user_id = $user_id
            AND
            n.repository_name = $repository_name
        DETACH DELETE n
        """

        self.execute_write(
            query,
            {
                "user_id": user_id,
                "repository_name": repository_name,
            },
        )

    def clear_database(self):

        logger.warning("Clearing Neo4j database.")

        self.execute_write(
            """
            MATCH (n)
            DETACH DELETE n
            """
        )

        logger.info("Database cleared.")