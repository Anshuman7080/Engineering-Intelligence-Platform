from app.parsing.symbol_table import SymbolTable


class SymbolTableBuilder:

    def build(
        self,
        parsed_repository: dict,
        repository_name: str,
    ) -> SymbolTable:

        table = SymbolTable()

        for file in parsed_repository["files"]:

            for function in file["functions"]:

                if function["is_method"]:

                    node_id = (
                        f"{repository_name}:"
                        f"{file['path']}:"
                        f"{function['class']}."
                        f"{function['name']}"
                    )

                else:

                    node_id = (
                        f"{repository_name}:"
                        f"{file['path']}:"
                        f"{function['name']}"
                    )

                if function["is_method"]:

                    
                    table.add(
                        function["name"],
                        node_id,
                    )

                    
                    table.add(
                        f"{function['class']}.{function['name']}",
                        node_id,
                    )

                else:

                    table.add(
                        function["name"],
                        node_id,
                    )

        return table