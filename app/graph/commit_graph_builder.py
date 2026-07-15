from app.graph.graph_data import GraphData
from app.graph.graph_models import (
    NodeType,
    RelationshipType,
)
from app.git.issue_extractor import IssueExtractor


class CommitGraphBuilder:

    def __init__(self):

        self.issue_extractor = IssueExtractor()

    def build(
        self,
        commits: list[dict],
        repository_name: str,
    ) -> GraphData:

        graph = GraphData()

        for commit in commits:

            commit_id = (
                f"{repository_name}:{commit['hash']}"
            )

            graph.add_node(
                label=NodeType.COMMIT.value,
                id=commit_id,
                repository=repository_name,
                hash=commit["hash"],
                author=commit["author"],
                email=commit["email"],
                date=str(commit["date"]),
                message=commit["message"],
            )

            
            issues = self.issue_extractor.extract(
                commit["message"]
            )

            for issue in issues:

                issue_id = (
                    f"{repository_name}:issue:{issue}"
                )

                graph.add_node(
                    label=NodeType.ISSUE.value,
                    id=issue_id,
                    repository=repository_name,
                    number=issue,
                )

                graph.add_relationship(
                    start_label=NodeType.COMMIT.value,
                    start_properties={
                        "id": commit_id,
                    },
                    end_label=NodeType.ISSUE.value,
                    end_properties={
                        "id": issue_id,
                    },
                    relationship=RelationshipType.FIXES.value,
                )

           
            for file in commit["files"]:

                normalized_file = file.replace("\\", "/")

                file_id = (
                    f"{repository_name}:{normalized_file}"
                )

                graph.add_relationship(
                    start_label=NodeType.COMMIT.value,
                    start_properties={
                        "id": commit_id,
                    },
                    end_label=NodeType.FILE.value,
                    end_properties={
                        "id": file_id,
                    },
                    relationship=RelationshipType.MODIFIES.value,
                )
        return graph