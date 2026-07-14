from app.parsing.ast_parser import ASTParser
from app.parsing.import_extractor import ImportExtractor


parser = ASTParser()

tree = parser.parse(
    "app/retrieval/retriever.py"
)

extractor = ImportExtractor()

imports = extractor.extract(tree)

for imp in imports:
    print(imp)