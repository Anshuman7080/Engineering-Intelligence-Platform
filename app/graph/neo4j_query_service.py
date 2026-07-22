from app.graph.graph_service import GraphService


class Neo4jQueryService:

    def __init__(self):

        self.graph_service = GraphService()


    def find_symbol(
        self,
        user_id: str,
        repository_name: str,
        name: str,
    ):

        query = """
        MATCH (n)

        WHERE
            (n:Function OR n:Method OR n:Class)
            AND n.user_id = $user_id
            AND n.repository_name = $repository_name
            AND n.name = $name

        RETURN
            labels(n) AS labels,
            n.id AS id,
            n.name AS name,
            n.path AS path
        """

        result = self.graph_service.execute(
            query,
            {
                "user_id": user_id,
                "repository_name": repository_name,
                "name": name,
            },
        )

        return [record.data() for record in result]


    def find_callers(
        self,
        user_id: str,
        repository_name: str,
        symbol_name: str,
    ):

        query = """
        MATCH (caller)-[:CALLS]->(callee)

        WHERE
            caller.user_id = $user_id
            AND caller.repository_name = $repository_name
            AND callee.user_id = $user_id
            AND callee.repository_name = $repository_name
            AND callee.name = $name

        RETURN
            labels(caller) AS caller_type,
            caller.name AS caller_name,
            caller.path AS path

        ORDER BY caller.path
        """

        result = self.graph_service.execute(
            query,
            {
                "user_id": user_id,
                "repository_name": repository_name,
                "name": symbol_name,
            },
        )

        return [record.data() for record in result]

    def find_callees(
        self,
        user_id: str,
        repository_name: str,
        symbol_name: str,
    ):

        query = """
        MATCH (caller)-[:CALLS]->(callee)

        WHERE
            caller.user_id = $user_id
            AND caller.repository_name = $repository_name
            AND callee.user_id = $user_id
            AND callee.repository_name = $repository_name
            AND caller.name = $name

        RETURN
            labels(callee) AS callee_type,
            callee.name AS callee_name,
            callee.path AS path

        ORDER BY callee.path
        """

        result = self.graph_service.execute(
            query,
            {
                "user_id": user_id,
                "repository_name": repository_name,
                "name": symbol_name,
            },
        )

        return [record.data() for record in result]


    def find_dependencies(
        self,
        user_id: str,
        repository_name: str,
        file_path: str,
    ):

        query = """
        MATCH (f:File)-[:DEPENDS_ON]->(dependency:File)

        WHERE
            f.user_id = $user_id
            AND f.repository_name = $repository_name
            AND dependency.user_id = $user_id
            AND dependency.repository_name = $repository_name
            AND f.path = $path

        RETURN
            dependency.path AS dependency

        ORDER BY dependency
        """

        result = self.graph_service.execute(
            query,
            {
                "user_id": user_id,
                "repository_name": repository_name,
                "path": file_path,
            },
        )

        return [record["dependency"] for record in result]

 
    def find_importers(
        self,
        user_id: str,
        repository_name: str,
        module_name: str,
    ):

        query = """
        MATCH (file:File)-[:IMPORTS]->(module:Module)

        WHERE
            file.user_id = $user_id
            AND file.repository_name = $repository_name
            AND module.user_id = $user_id
            AND module.repository_name = $repository_name
            AND module.name = $name

        RETURN
            file.path AS file

        ORDER BY file
        """

        result = self.graph_service.execute(
            query,
            {
                "user_id": user_id,
                "repository_name": repository_name,
                "name": module_name,
            },
        )

        return [record["file"] for record in result]

   
    def find_commits_for_file(
        self,
        user_id: str,
        repository_name: str,
        file_path: str,
    ):

        query = """
        MATCH (c:Commit)-[:MODIFIES]->(f:File)

        WHERE
            c.user_id = $user_id
            AND c.repository_name = $repository_name
            AND f.user_id = $user_id
            AND f.repository_name = $repository_name
            AND f.path = $path

        RETURN
            c.hash AS hash,
            c.author AS author,
            c.date AS date,
            c.message AS message

        ORDER BY c.date DESC
        """

        result = self.graph_service.execute(
            query,
            {
                "user_id": user_id,
                "repository_name": repository_name,
                "path": file_path,
            },
        )

        return [record.data() for record in result]

    def find_files_for_commit(
        self,
        user_id: str,
        repository_name: str,
        commit_hash: str,
    ):

        query = """
        MATCH (c:Commit)-[:MODIFIES]->(f:File)

        WHERE
            c.user_id = $user_id
            AND c.repository_name = $repository_name
            AND f.user_id = $user_id
            AND f.repository_name = $repository_name
            AND c.hash = $hash

        RETURN
            f.path AS file

        ORDER BY file
        """

        result = self.graph_service.execute(
            query,
            {
                "user_id": user_id,
                "repository_name": repository_name,
                "hash": commit_hash,
            },
        )

        return [record["file"] for record in result]

  
    def find_issue_commits(
        self,
        user_id: str,
        repository_name: str,
        issue_number: int,
    ):

        query = """
        MATCH (c:Commit)-[:FIXES]->(i:Issue)

        WHERE
            c.user_id = $user_id
            AND c.repository_name = $repository_name
            AND i.user_id = $user_id
            AND i.repository_name = $repository_name
            AND i.number = $issue

        RETURN
            c.hash AS hash,
            c.author AS author,
            c.date AS date,
            c.message AS message

        ORDER BY c.date DESC
        """

        result = self.graph_service.execute(
            query,
            {
                "user_id": user_id,
                "repository_name": repository_name,
                "issue": issue_number,
            },
        )

        return [record.data() for record in result]

    def find_issue_changes(
        self,
        user_id: str,
        repository_name: str,
        issue_number: int,
    ):

        query = """
        MATCH (i:Issue)<-[:FIXES]-(c:Commit)-[:MODIFIES]->(f:File)

        WHERE
            i.user_id = $user_id
            AND i.repository_name = $repository_name
            AND c.user_id = $user_id
            AND c.repository_name = $repository_name
            AND f.user_id = $user_id
            AND f.repository_name = $repository_name
            AND i.number = $issue

        RETURN DISTINCT
            f.path AS file

        ORDER BY file
        """

        result = self.graph_service.execute(
            query,
            {
                "user_id": user_id,
                "repository_name": repository_name,
                "issue": issue_number,
            },
        )

        return [record["file"] for record in result]