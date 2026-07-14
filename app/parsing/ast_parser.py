import ast
from pathlib import Path


class ASTParser:

    def parse(self,file_path:str | Path):

        file_path=Path(file_path)

        source=file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )


        tree=ast.parse(source)



        return tree
