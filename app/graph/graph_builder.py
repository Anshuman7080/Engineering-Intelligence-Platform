from app.graph.graph_data import GraphData
from app.graph.graph_models import (
    NodeType,
    RelationshipType,
)
from app.parsing.dependency_resolver import DependencyResolver
from app.parsing.symbol_table_builder import SymbolTableBuilder
from app.parsing.symbol_resolver import SymbolResolver

class GraphBuilder:

    def __init__(
    self,
    repository_root: str,
    ):

        self.dependency_resolver = DependencyResolver(
            repository_root
        )

    def build(
        self,
        parsed_repository: dict,
        repository_name: str,
    ) -> GraphData:

        graph = GraphData()

        symbol_table = SymbolTableBuilder().build(
            parsed_repository,
            repository_name,
        )

        self.symbol_resolver = SymbolResolver(
            symbol_table
        )

        graph.add_node(
            label=NodeType.REPOSITORY.value,
            id=repository_name,
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
                repository_name,
            )


            self._add_dependencies(
                graph,
                file,
                repository_name,
            )

            self._add_classes(
                graph,
                file,
                repository_name,
            )

            self._add_functions(
                graph,
                file,
                repository_name,
            )

            self._add_calls(
                graph,
                file,
                repository_name,
            )

        return graph
    

    def _add_file(
        self,
        graph: GraphData,
        repository_name: str,
        file: dict,
    ):

        file_id = f"{repository_name}:{file['path']}"

        graph.add_node(
            label=NodeType.FILE.value,
            id=file_id,
            repository=repository_name,
            path=file["path"],
        )

        graph.add_relationship(
            start_label=NodeType.REPOSITORY.value,
            start_properties={
                "id": repository_name,
            },
            end_label=NodeType.FILE.value,
            end_properties={
                "id": file_id,
            },
            relationship=RelationshipType.CONTAINS.value,
        )

        
    def _add_imports(
        self,
        graph: GraphData,
        file: dict,
        repository_name: str,
         ):

            file_id = f"{repository_name}:{file['path']}"

            for imp in file["imports"]:

                module = imp.get("module")

                if not module:
                    continue

                module_id = f"{repository_name}:{module}"

                graph.add_node(
                    label=NodeType.MODULE.value,
                    id=module_id,
                    repository=repository_name,
                    name=module,
                )

                graph.add_relationship(
                    start_label=NodeType.FILE.value,
                    start_properties={
                        "id": file_id,
                    },
                    end_label=NodeType.MODULE.value,
                    end_properties={
                        "id": module_id,
                    },
                    relationship=RelationshipType.IMPORTS.value,
                )
      
    def _add_dependencies(
    self,
    graph: GraphData,
    file: dict,
    repository_name: str,
    ):

        source_file_id = (
            f"{repository_name}:{file['path']}"
        )

        for imp in file["imports"]:

            module = imp.get("module")

            if not module:
                continue

            dependency = self.dependency_resolver.resolve(
                module
            )

            if dependency is None:
                continue

            target_file_id = (
                f"{repository_name}:{dependency}"
            )

            graph.add_relationship(
                start_label=NodeType.FILE.value,
                start_properties={
                    "id": source_file_id,
                },
                end_label=NodeType.FILE.value,
                end_properties={
                    "id": target_file_id,
                },
                relationship=RelationshipType.DEPENDS_ON.value,
            )

    def _add_classes(
    self,
    graph: GraphData,
    file: dict,
    repository_name: str,
    ):

        file_id = f"{repository_name}:{file['path']}"

        for cls in file["classes"]:

            class_id = (
                f"{repository_name}:"
                f"{file['path']}:"
                f"{cls['name']}"
            )

            graph.add_node(
                label=NodeType.CLASS.value,
                id=class_id,
                repository=repository_name,
                path=file["path"],
                name=cls["name"],
            )

            graph.add_relationship(
                start_label=NodeType.FILE.value,
                start_properties={
                    "id": file_id,
                },
                end_label=NodeType.CLASS.value,
                end_properties={
                    "id": class_id,
                },
                relationship=RelationshipType.CONTAINS.value,
            ) 

    def _add_functions(
    self,
    graph: GraphData,
    file: dict,
    repository_name: str,
     ):

        file_id = f"{repository_name}:{file['path']}"

        for function in file["functions"]:

            if function["is_method"]:

                node_label = NodeType.METHOD.value

                node_id = (
                    f"{repository_name}:"
                    f"{file['path']}:"
                    f"{function['class']}."
                    f"{function['name']}"
                )

            else:

                node_label = NodeType.FUNCTION.value

                node_id = (
                    f"{repository_name}:"
                    f"{file['path']}:"
                    f"{function['name']}"
                )

            graph.add_node(
                label=node_label,
                id=node_id,
                repository=repository_name,
                path=file["path"],
                name=function["name"],
            )

            graph.add_relationship(
                start_label=NodeType.FILE.value,
                start_properties={
                    "id": file_id,
                },
                end_label=node_label,
                end_properties={
                    "id": node_id,
                },
                relationship=RelationshipType.DECLARES.value,
            )

    def _add_calls(
    self,
    graph: GraphData,
    file: dict,
    repository_name: str,
    ):

        for call in file["calls"]:

          
            if call["caller_class"]:

                caller_id = (
                    f"{repository_name}:"
                    f"{file['path']}:"
                    f"{call['caller_class']}."
                    f"{call['caller']}"
                )

                start_label = NodeType.METHOD.value

            else:

                caller_id = (
                    f"{repository_name}:"
                    f"{file['path']}:"
                    f"{call['caller']}"
                )

                start_label = NodeType.FUNCTION.value

            
            callee_id = self.symbol_resolver.resolve(
                symbol_name=call["callee"],
                class_name=call["caller_class"],
            )

          
            if callee_id is None:
                continue

           
            last_part = callee_id.split(":")[-1]

            if "." in last_part:
                end_label = NodeType.METHOD.value
            else:
                end_label = NodeType.FUNCTION.value

            
            graph.add_relationship(
                start_label=start_label,
                start_properties={
                    "id": caller_id,
                },
                end_label=end_label,
                end_properties={
                    "id": callee_id,
                },
                relationship=RelationshipType.CALLS.value,
            ) 