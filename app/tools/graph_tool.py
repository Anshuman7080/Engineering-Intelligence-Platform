from app.graph.neo4j_query_service import Neo4jQueryService
from app.tools.graph_query_types import GraphQueryType
from app.tools.tool_response import ToolResponse


class GraphTool:

    def __init__(self):
        self.query_service = Neo4jQueryService()

    def _get(self, kwargs, *keys):

        for key in keys:
            value = kwargs.get(key)

            if value is not None:
                return value

        raise ValueError(
            f"Missing required argument. Expected one of {keys}"
        )

    def execute(
        self,
        query_type: GraphQueryType,
        **kwargs,
    ):

        user_id = self._get(kwargs, "user_id")
        repository_name = self._get(kwargs, "repository_name")

        if query_type == GraphQueryType.FIND_SYMBOL:

            symbol = self._get(
                kwargs,
                "symbol_name",
                "name",
            )

            results = self.query_service.find_symbol(
                user_id=user_id,
                repository_name=repository_name,
                name=symbol,
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )

        elif query_type == GraphQueryType.FIND_CALLERS:

            symbol = self._get(
                kwargs,
                "symbol_name",
            )

            results = self.query_service.find_callers(
                user_id=user_id,
                repository_name=repository_name,
                symbol_name=symbol,
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )

        elif query_type == GraphQueryType.FIND_CALLEES:

            symbol = self._get(
                kwargs,
                "symbol_name",
            )

            results = self.query_service.find_callees(
                user_id=user_id,
                repository_name=repository_name,
                symbol_name=symbol,
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )

        elif query_type == GraphQueryType.FIND_DEPENDENCIES:

            file_path = self._get(
                kwargs,
                "file_path",
            )

            results = self.query_service.find_dependencies(
                user_id=user_id,
                repository_name=repository_name,
                file_path=file_path,
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )

        elif query_type == GraphQueryType.FIND_IMPORTERS:

            module_name = self._get(
                kwargs,
                "module_name",
            )

            results = self.query_service.find_importers(
                user_id=user_id,
                repository_name=repository_name,
                module_name=module_name,
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )

        elif query_type == GraphQueryType.FIND_COMMITS_FOR_FILE:

            file_path = self._get(
                kwargs,
                "file_path",
            )

            results = self.query_service.find_commits_for_file(
                user_id=user_id,
                repository_name=repository_name,
                file_path=file_path,
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )

        elif query_type == GraphQueryType.FIND_FILES_FOR_COMMIT:

            commit_hash = self._get(
                kwargs,
                "commit_hash",
            )

            results = self.query_service.find_files_for_commit(
                user_id=user_id,
                repository_name=repository_name,
                commit_hash=commit_hash,
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )

        elif query_type == GraphQueryType.FIND_ISSUE_COMMITS:

            issue_number =int( self._get(
                kwargs,
                "issue_number",
            ))

            results = self.query_service.find_issue_commits(
                user_id=user_id,
                repository_name=repository_name,
                issue_number=issue_number,
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )

        elif query_type == GraphQueryType.FIND_ISSUE_CHANGES:

            issue_number =int( self._get(
                kwargs,
                "issue_number",
            ))

            results = self.query_service.find_issue_changes(
                user_id=user_id,
                repository_name=repository_name,
                issue_number=issue_number,
            )

            return ToolResponse(
                tool="graph",
                query_type=query_type.value,
                results=results,
            )

        raise ValueError(
            f"Unsupported query type: {query_type}"
        )