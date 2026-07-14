import ast


class ClassExtractor(ast.NodeVisitor):

    def __init__(self):

        self.classes = []

    def visit_ClassDef(self, node: ast.ClassDef):

        self.classes.append(
            {
                "name": node.name,
                "line": node.lineno,
            }
        )

        self.generic_visit(node)

    def extract(
        self,
        tree: ast.AST,
    ):

        self.classes = []

        self.visit(tree)

        return self.classes