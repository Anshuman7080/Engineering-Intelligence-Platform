import ast


class FunctionExtractor(ast.NodeVisitor):

    def __init__(self):

        self.functions = []
        self.current_class = None

    def visit_ClassDef(self, node: ast.ClassDef):

        previous_class = self.current_class
        self.current_class = node.name

        self.generic_visit(node)

        self.current_class = previous_class

    def visit_FunctionDef(self, node: ast.FunctionDef):

        self.functions.append(
            {
                "name": node.name,
                "line": node.lineno,
                "class": self.current_class,
                "is_method": self.current_class is not None,
            }
        )

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):

        self.functions.append(
            {
                "name": node.name,
                "line": node.lineno,
                "class": self.current_class,
                "is_method": self.current_class is not None,
            }
        )

        self.generic_visit(node)

    def extract(
        self,
        tree: ast.AST,
    ):

        self.functions = []
        self.current_class = None

        self.visit(tree)

        return self.functions