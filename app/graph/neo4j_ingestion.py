from collections import defaultdict

from app.graph.graph_data import GraphData
from app.graph.graph_service import GraphService


class Neo4jIngestionService:

    def __init__(self):

        self.graph_service = GraphService()

    def ingest(
        self,
        graph_data: GraphData,
    ):

        self._insert_nodes(graph_data.nodes)

        self._insert_relationships(graph_data.relationships)


    def _insert_nodes(
            self,
            nodes,
    ) :

        grouped=defaultdict(list)

        for node in nodes:

            grouped[node.label].append(
                node.properties
            )

        for label,rows in grouped.items():
            self._insert_node_batch(
                label,
                rows,
            ) 



    def _insert_node_batch(
        self,
        label: str,
        rows: list[dict],
    ):

        if not rows:
            return

        keys = list(rows[0].keys())

        merge_keys = ", ".join(
            f"{k}: row.{k}"
            for k in keys
        )

        query = f"""
        UNWIND $rows AS row

        MERGE (n:{label} {{
            {merge_keys}
        }})
        """

        self.graph_service.execute_write(
            query,
            {
                "rows": rows,
            },
        )


    def _insert_relationships(
        self,
        relationships,
    ):

        grouped = defaultdict(list)

        for relationship in relationships:

            grouped[
                relationship.relationship
            ].append(
                relationship
            )

        for relation, rows in grouped.items():

            self._insert_relationship_batch(
                relation,
                rows,
            ) 

    def _insert_relationship_batch(
        self,
        relationship: str,
        rows,
    ):

        if not rows:
            return

        start_label = rows[0].start_label
        end_label = rows[0].end_label

        formatted_rows = []

        for row in rows:

            formatted_rows.append(
                {
                    "start": row.start_properties,
                    "end": row.end_properties,
                }
            )

        start_keys = rows[0].start_properties.keys()
        end_keys = rows[0].end_properties.keys()

        start_match = " AND ".join(
            f"a.{k}=row.start.{k}"
            for k in start_keys
        )

        end_match = " AND ".join(
            f"b.{k}=row.end.{k}"
            for k in end_keys
        )

        query = f"""
        UNWIND $rows AS row

        MATCH (a:{start_label})

        WHERE {start_match}

        MATCH (b:{end_label})

        WHERE {end_match}

        MERGE (a)-[:{relationship}]->(b)
        """

        self.graph_service.execute_write(
            query,
            {
                "rows": formatted_rows,
            },
        )           