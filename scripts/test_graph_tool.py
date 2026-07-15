from pprint import pprint

from app.tools.graph_tool import GraphTool
from app.tools.graph_query_types import GraphQueryType


tool = GraphTool()


print("\nSymbol\n")

pprint(
    tool.execute(
        query_type=GraphQueryType.FIND_SYMBOL,
        name="BaseRetriever",
    )
)


print("\nCallers\n")

pprint(
    tool.execute(
        query_type=GraphQueryType.FIND_CALLERS,
        symbol_name="invoke",
    )
)


# print("\nDependencies\n")

# pprint(
#     tool.execute(
#         query_type=GraphQueryType.FIND_DEPENDENCIES,
#         file_path="libs/core/langchain_core/retrievers.py",
#     )
# )