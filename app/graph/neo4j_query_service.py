from app.graph.graph_service import GraphService


class Neo4jQueryService:

    def __init__(self):

        self.graph_service=GraphService()


    def find_symbol(
    self,
    name: str,
    ):

        query = """
        MATCH (n)
        WHERE
            (n:Function OR n:Method OR n:Class)
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
                "name": name,
            },
        )

        return [record.data() for record in result]
    
    def find_callers(
    self,
    symbol_name: str,
    ):

        query = """
        MATCH (caller)-[:CALLS]->(callee)

        WHERE callee.name = $name

        RETURN
            labels(caller) AS caller_type,
            caller.name AS caller_name,
            caller.path AS path

        ORDER BY caller.path
        """

        result = self.graph_service.execute(
            query,
            {
                "name": symbol_name,
            },
        )

        return [
            record.data()
            for record in result
        ]
 
    def find_callees(
    self,
    symbol_name: str,
    ):

        query = """
        MATCH (caller)-[:CALLS]->(callee)

        WHERE caller.name = $name

        RETURN
            labels(callee) AS callee_type,
            callee.name AS callee_name,
            callee.path AS path

        ORDER BY callee.path
        """

        result = self.graph_service.execute(
            query,
            {
                "name": symbol_name,
            },
        )

        return [
            record.data()
            for record in result
        ] 

    def find_dependencies(
    self,
    file_path: str,
    ):

        query = """
        MATCH (f:File)-[:DEPENDS_ON]->(dependency:File)

        WHERE f.path = $path

        RETURN
            dependency.path AS dependency

        ORDER BY dependency
        """

        result = self.graph_service.execute(
            query,
            {
                "path": file_path,
            },
        )

        return [
            record["dependency"]
            for record in result
        ] 

    def find_importers(
    self,
    module_name: str,
    ):

        query = """
        MATCH (file:File)-[:IMPORTS]->(module:Module)

        WHERE module.name = $name

        RETURN
            file.path AS file

        ORDER BY file
        """

        result = self.graph_service.execute(
            query,
            {
                "name": module_name,
            },
        )

        return [
            record["file"]
            for record in result
        ] 
    

    def find_commits_for_file(
        self,
        file_path: str,
    ):

        query = """
        MATCH (c:Commit)-[:MODIFIES]->(f:File)

        WHERE f.path = $path

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
                "path": file_path,
            },
        )

        return [
            record.data()
            for record in result
        ]    

    def find_files_for_commit(
    self,
    commit_hash: str,
    ):

        query = """
        MATCH (c:Commit)-[:MODIFIES]->(f:File)

        WHERE c.hash = $hash

        RETURN
            f.path AS file

        ORDER BY file
        """

        result = self.graph_service.execute(
            query,
            {
                "hash": commit_hash,
            },
        )

        return [
            record["file"]
            for record in result
        ]

    def find_issue_commits(
    self,
    issue_number: int,
    ):

        query = """
        MATCH (c:Commit)-[:FIXES]->(i:Issue)

        WHERE i.number = $issue

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
                "issue": issue_number,
            },
        )

        return [
            record.data()
            for record in result
        ]

    def find_issue_changes(
    self,
    issue_number: int,
    ):

        query = """
        MATCH (i:Issue)<-[:FIXES]-(c:Commit)-[:MODIFIES]->(f:File)

        WHERE i.number = $issue

        RETURN DISTINCT
            f.path AS file

        ORDER BY file
        """

        result = self.graph_service.execute(
            query,
            {
                "issue": issue_number,
            },
        )

        return [
            record["file"]
            for record in result
        ]






