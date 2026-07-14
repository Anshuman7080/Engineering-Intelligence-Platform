import ast


class ImportExtractor(ast.NodeVisitor):

    def __init__(self):

        self.imports = []

    def visit_Import(self, node: ast.Import):

        for alias in node.names:

            self.imports.append(
                {
                    "module": alias.name,
                    "alias": alias.asname,
                }
            )

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):

        module = node.module or ""

        for alias in node.names:

            self.imports.append(
                {
                    "module": module,
                    "name": alias.name,
                    "alias": alias.asname,
                }
            )

        self.generic_visit(node)

    def extract(self, tree: ast.AST):

        self.imports = []

        self.visit(tree)

        return self.imports