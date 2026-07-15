from app.graph.neo4j_query_service import Neo4jQueryService
from app.tools.graph_query_types import GraphQueryType


class GraphTool:

    def __init__(self):

        self.query_service = Neo4jQueryService()

    def execute(
        self,
        query_type: GraphQueryType,
        **kwargs,
    ):

        if query_type == GraphQueryType.FIND_SYMBOL:

            return self.query_service.find_symbol(
                kwargs["name"]
            )

        elif query_type == GraphQueryType.FIND_CALLERS:

            return self.query_service.find_callers(
                kwargs["symbol_name"]
            )

        elif query_type == GraphQueryType.FIND_CALLEES:

            return self.query_service.find_callees(
                kwargs["symbol_name"]
            )

        elif query_type == GraphQueryType.FIND_DEPENDENCIES:

            return self.query_service.find_dependencies(
                kwargs["file_path"]
            )

        elif query_type == GraphQueryType.FIND_IMPORTERS:

            return self.query_service.find_importers(
                kwargs["module_name"]
            )

        elif query_type == GraphQueryType.FIND_COMMITS_FOR_FILE:

            return self.query_service.find_commits_for_file(
                kwargs["file_path"]
            )

        elif query_type == GraphQueryType.FIND_FILES_FOR_COMMIT:

            return self.query_service.find_files_for_commit(
                kwargs["commit_hash"]
            )

        elif query_type == GraphQueryType.FIND_ISSUE_COMMITS:

            return self.query_service.find_issue_commits(
                kwargs["issue_number"]
            )

        elif query_type == GraphQueryType.FIND_ISSUE_CHANGES:

            return self.query_service.find_issue_changes(
                kwargs["issue_number"]
            )

        raise ValueError(
            f"Unsupported query type: {query_type}"
        )