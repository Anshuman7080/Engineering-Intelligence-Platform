import ast


class CallExtractor(ast.NodeVisitor):

    def __init__(self):

        self.calls = []

        self.current_function = None
        self.current_class = None

    def visit_ClassDef(
        self,
        node: ast.ClassDef,
    ):

        previous = self.current_class

        self.current_class = node.name

        self.generic_visit(node)

        self.current_class = previous

    def visit_FunctionDef(
        self,
        node: ast.FunctionDef,
    ):

        previous = self.current_function

        self.current_function = node.name

        self.generic_visit(node)

        self.current_function = previous

    def visit_AsyncFunctionDef(
        self,
        node: ast.AsyncFunctionDef,
    ):

        previous = self.current_function

        self.current_function = node.name

        self.generic_visit(node)

        self.current_function = previous

    def visit_Call(
        self,
        node: ast.Call,
    ):

        called_function = self._get_call_name(node.func)

        if called_function and self.current_function:

            self.calls.append(
                {
                    "caller": self.current_function,
                    "caller_class": self.current_class,
                    "callee": called_function,
                    "line": node.lineno,
                }
            )

        self.generic_visit(node)

    def _get_call_name(
        self,
        node,
    ):

        if isinstance(node, ast.Name):

            return node.id

        if isinstance(node, ast.Attribute):

            return node.attr

        return None

    def extract(
        self,
        tree: ast.AST,
    ):

        self.calls = []

        self.current_function = None
        self.current_class = None

        self.visit(tree)

        return self.calls