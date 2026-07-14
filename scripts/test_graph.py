from app.graph.graph_service import GraphService


graph = GraphService()

result = graph.execute(
    """
    RETURN 'Neo4j Connected Successfully' AS message
    """
)

print(result[0]["message"])

graph.close()