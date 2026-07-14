from app.parsing.repository_parser import RepositoryParser
from app.graph.graph_builder import GraphBuilder


parser = RepositoryParser()

parsed = parser.parse_repository(
    "data/repositories/langchain.git"
)

builder = GraphBuilder()

graph = builder.build(
    parsed,
    "langchain",
)

print(len(graph.nodes))
print(len(graph.relationships))

print(graph.nodes[0])
print(graph.relationships[0])