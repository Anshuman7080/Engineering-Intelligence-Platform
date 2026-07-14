from app.graph.graph_data import GraphData
from app.graph.graph_models import (
    NodeType,
    RelationshipType,
)


class GraphBuilder:

    def build(
        self,
        parsed_repository: dict,
        repository_name: str,
    ) -> GraphData:

        graph = GraphData()

        graph.add_node(
            label=NodeType.REPOSITORY.value,
            name=repository_name,
        )

        for file in parsed_repository["files"]:

            self._add_file(
                graph,
                repository_name,
                file,
            )

            self._add_imports(
                graph,
                file,
            )

            self._add_classes(
                graph,
                file,
            )

            self._add_functions(
                graph,
                file,
            )

            self._add_calls(
                graph,
                file,
            )

        return graph
    

    def _add_file(
        self,
        graph: GraphData,
        repository_name: str,
        file: dict,
    ):

        graph.add_node(
            label=NodeType.FILE.value,
            path=file["path"],
        )

        graph.add_relationship(
            start_label=NodeType.REPOSITORY.value,
            start_properties={
                "name": repository_name,
            },
            end_label=NodeType.FILE.value,
            end_properties={
                "path": file["path"],
            },
            relationship=RelationshipType.CONTAINS.value,
        )

    
    
    def _add_imports(
        self,
        graph: GraphData,
        file: dict,
    ):

        for imp in file["imports"]:

            module = imp.get("module")

            if not module:
                continue

            graph.add_node(
                label=NodeType.MODULE.value,
                name=module,
            )

            graph.add_relationship(
                start_label=NodeType.FILE.value,
                start_properties={
                    "path": file["path"],
                },
                end_label=NodeType.MODULE.value,
                end_properties={
                    "name": module,
                },
                relationship=RelationshipType.IMPORTS.value,
            )   

    def _add_classes(
        self,
        graph: GraphData,
        file: dict,
    ):

        for cls in file["classes"]:

            graph.add_node(
                label=NodeType.CLASS.value,
                name=cls["name"],
            )

            graph.add_relationship(
                start_label=NodeType.FILE.value,
                start_properties={
                    "path": file["path"],
                },
                end_label=NodeType.CLASS.value,
                end_properties={
                    "name": cls["name"],
                },
                relationship=RelationshipType.CONTAINS.value,
            )      

    def _add_functions(
        self,
        graph: GraphData,
        file: dict,
    ):

        for function in file["functions"]:

            label = (
                NodeType.METHOD.value
                if function["is_method"]
                else NodeType.FUNCTION.value
            )

            graph.add_node(
                label=label,
                name=function["name"],
            )

            graph.add_relationship(
                start_label=NodeType.FILE.value,
                start_properties={
                    "path": file["path"],
                },
                end_label=label,
                end_properties={
                    "name": function["name"],
                },
                relationship=RelationshipType.DECLARES.value,
            )    


    def _add_calls(
        self,
        graph: GraphData,
        file: dict,
    ):

        for call in file["calls"]:

            graph.add_relationship(
                start_label=NodeType.FUNCTION.value,
                start_properties={
                    "name": call["caller"],
                },
                end_label=NodeType.FUNCTION.value,
                end_properties={
                    "name": call["callee"],
                },
                relationship=RelationshipType.CALLS.value,
            )               