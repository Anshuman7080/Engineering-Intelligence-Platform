from git import Repo
from pathlib import Path


class GitHistoryParser:

    def parse(
        self,
        repository_path: str,
    ) -> list[dict]:

        repository = Repo(Path(repository_path))

        commits = []

        for commit in repository.iter_commits():
           

            changed_files = []

           
            if not commit.parents:

                changed_files = list(commit.stats.files.keys())

            else:

                changed_files = list(commit.stats.files.keys())

            commits.append(
                {
                    "hash": commit.hexsha,
                    "author": commit.author.name,
                    "email": commit.author.email,
                    "date": commit.committed_datetime,
                    "message": commit.message.strip(),
                    "files": changed_files,
                }
            )

        return commits