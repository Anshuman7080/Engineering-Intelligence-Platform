from collections import defaultdict
from itertools import islice

from app.graph.graph_data import GraphData
from app.graph.graph_service import GraphService
from app.core.logger import logger


class Neo4jIngestionService:

    def __init__(self):

        self.graph_service = GraphService()

        self.batch_size = 1000

    def ingest(
        self,
        graph_data: GraphData,
    ):

        logger.info("Inserting nodes...")
        self._insert_nodes(graph_data.nodes)

        logger.info("Inserting relationships...")
        self._insert_relationships(
            graph_data.relationships
        )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _chunk(
        self,
        items,
    ):

        iterator = iter(items)

        while True:

            batch = list(
                islice(
                    iterator,
                    self.batch_size,
                )
            )

            if not batch:
                break

            yield batch

    # ---------------------------------------------------------
    # Nodes
    # ---------------------------------------------------------

    def _insert_nodes(
        self,
        nodes,
    ):

        grouped = defaultdict(list)

        for node in nodes:
            grouped[node.label].append(node.properties)

        for label, rows in grouped.items():

            total = len(rows)

            logger.info(
                f"{label}: {total} nodes"
            )

            inserted = 0

            for batch in self._chunk(rows):

                self._insert_node_batch(
                    label,
                    batch,
                )

                inserted += len(batch)

                logger.info(
                    f"{label}: {inserted}/{total}"
                )

    def _insert_node_batch(
        self,
        label: str,
        rows: list[dict],
    ):

        if not rows:
            return

        query = f"""
        UNWIND $rows AS row

        MERGE (n:{label} {{
            id: row.id
        }})

        SET n += row
        """

        self.graph_service.execute_write(
            query,
            {
                "rows": rows,
            },
        )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    def _insert_relationships(
        self,
        relationships,
    ):

        grouped = defaultdict(list)

        for relationship in relationships:

            key = (
                relationship.relationship,
                relationship.start_label,
                relationship.end_label,
            )

            grouped[key].append(relationship)

        for (
        relation,
        start_label,
        end_label,
    ), rows in grouped.items():

            total = len(rows)

            logger.info(
                f"{relation}: {total} relationships"
            )

            inserted = 0

            for batch in self._chunk(rows):

                self._insert_relationship_batch(
                    relation,
                    start_label,
                    end_label,
                    batch,
                )

                inserted += len(batch)

                logger.info(
                    f"{relation}: {inserted}/{total}"
                )

    def _insert_relationship_batch(
        self,
        relationship: str,
        start_label:str,
        end_label:str,
        rows,
    ):

        if not rows:
            return

        

        formatted_rows = []

        for row in rows:

            formatted_rows.append(
                {
                    "start_id": row.start_properties["id"],
                    "end_id": row.end_properties["id"],
                }
            )

        query = f"""
        UNWIND $rows AS row

        MATCH (a:{start_label} {{
            id: row.start_id
        }})

        MATCH (b:{end_label} {{
            id: row.end_id
        }})

        MERGE (a)-[:{relationship}]->(b)
        """

        self.graph_service.execute_write(
            query,
            {
                "rows": formatted_rows,
            },
        )