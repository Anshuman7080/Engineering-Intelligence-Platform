from app.git.git_history_parser import GitHistoryParser
from app.graph.commit_graph_builder import CommitGraphBuilder

parser = GitHistoryParser()

commits = parser.parse(
    "data/repositories/langchain.git"
)

builder = CommitGraphBuilder()

graph = builder.build(
    commits,
    "langchain"
)

print("Nodes :", len(graph.nodes))
print("Relationships :", len(graph.relationships))

print()
print(graph.nodes[0])
print()
print(graph.relationships[0])