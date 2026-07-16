from app.tools.graph_tool import GraphTool
from app.tools.vector_tool import VectorTool
from app.tools.graph_query_types import GraphQueryType


# graph = GraphTool()

# response = graph.execute(
#     GraphQueryType.FIND_SYMBOL,
#     name="Runnable",
# )

# print(response)


vector = VectorTool()

response = vector.search(
    query="How does Runnable.invoke work?",
    repository_name="langchain.git",
)

print(response)