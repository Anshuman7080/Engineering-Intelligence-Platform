from app.parsing.repository_parser import RepositoryParser
from app.parsing.symbol_table_builder import SymbolTableBuilder

repository = RepositoryParser().parse_repository(
    "data/repositories/langchain.git"
)

table = SymbolTableBuilder().build(
    repository,
    "langchain",
)

print("Symbols:", len(table))

print()

print("lookup(search)")
print(table.lookup("search"))

print()

print("lookup(invoke)")
print(table.lookup("invoke"))