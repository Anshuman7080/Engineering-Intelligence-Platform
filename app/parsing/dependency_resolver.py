from pathlib import Path


class DependencyResolver:

    def __init__(
        self,
        repository_root: str,
    ):

        self.repository_root = Path(repository_root)

    def resolve(
        self,
        module: str,
    ) -> str | None:

        if not module:
            return None

        relative_path = Path(
            *module.split(".")
        ).with_suffix(".py")

        full_path = self.repository_root / relative_path

        if full_path.exists():

            return relative_path.as_posix()

        init_path = (
            self.repository_root
            / Path(*module.split("."))
            / "__init__.py"
        )

        if init_path.exists():

            return (
                Path(*module.split("."))
                / "__init__.py"
            ).as_posix()

        return None