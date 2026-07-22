from app.parsing.symbol_table import SymbolTable


class SymbolResolver:

    def __init__(
        self,
        symbol_table: SymbolTable,
    ):
        self.symbol_table = symbol_table

    def resolve(
        self,
        symbol_name: str,
        class_name: str | None = None,
    ) -> str | None:

        if class_name:

            full_name = (
                f"{class_name}.{symbol_name}"
            )

            candidates = self.symbol_table.lookup(
                full_name
            )

            if len(candidates) == 1:
                return candidates[0]

        candidates = self.symbol_table.lookup(
            symbol_name
        )

        if len(candidates) == 1:
            return candidates[0]

        return None