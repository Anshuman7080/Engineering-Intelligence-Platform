from app.graph.neo4j_query_service import Neo4jQueryService
from app.tools.graph_query_types import GraphQueryType
from app.tools.tool_response import ToolResponse


class GraphTool:

    def __init__(self):

        self.query_service = Neo4jQueryService()

    def execute(
        self,
        query_type: GraphQueryType,
        **kwargs,
    ):

        if query_type == GraphQueryType.FIND_SYMBOL:

            results= self.query_service.find_symbol(
                kwargs["name"]
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )

        elif query_type == GraphQueryType.FIND_CALLERS:

            results= self.query_service.find_callers(
                kwargs["symbol_name"]
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )


        elif query_type == GraphQueryType.FIND_CALLEES:

            results= self.query_service.find_callees(
                kwargs["symbol_name"]
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )


        elif query_type == GraphQueryType.FIND_DEPENDENCIES:

            results= self.query_service.find_dependencies(
                kwargs["file_path"]
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )


        elif query_type == GraphQueryType.FIND_IMPORTERS:

            results= self.query_service.find_importers(
                kwargs["module_name"]
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )


        elif query_type == GraphQueryType.FIND_COMMITS_FOR_FILE:

            results= self.query_service.find_commits_for_file(
                kwargs["file_path"]
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )


        elif query_type == GraphQueryType.FIND_FILES_FOR_COMMIT:

            results= self.query_service.find_files_for_commit(
                kwargs["commit_hash"]
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )


        elif query_type == GraphQueryType.FIND_ISSUE_COMMITS:

            results= self.query_service.find_issue_commits(
                kwargs["issue_number"]
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )


        elif query_type == GraphQueryType.FIND_ISSUE_CHANGES:

            results= self.query_service.find_issue_changes(
                kwargs["issue_number"]
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )


        raise ValueError(
            f"Unsupported query type: {query_type}"
        )