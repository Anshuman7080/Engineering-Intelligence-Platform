import ast

from app.parsing.ast_parser import ASTParser


parser = ASTParser()

tree = parser.parse(
    "app/retrieval/retriever.py"
)

print(type(tree))

print(ast.dump(tree, indent=4))