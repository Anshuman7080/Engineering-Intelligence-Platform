class SymbolTable:

    def __init__(self):

        self.table = {}

    def add(
        self,
        symbol: str,
        node_id: str,
    ):

        self.table.setdefault(symbol, []).append(node_id)

    def lookup(
        self,
        symbol: str,
    ):

        return self.table.get(symbol, [])

    def __contains__(
        self,
        symbol: str,
    ):

        return symbol in self.table

    def __len__(self):

        return len(self.table)