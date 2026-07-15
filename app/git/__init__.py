import subprocess
from datetime import datetime


class GitHistoryParser:

    def parse(
        self,
        repository_path: str,
    ) -> list[dict]:

        command = [
            "git",
            "-C",
            repository_path,
            "log",
            "--name-only",
            "--pretty=format:%H|%an|%ad|%s",
            "--date=iso",
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

        commits = []

        current_commit = None

        for line in result.stdout.splitlines():

            line = line.strip()

            if not line:
                continue

            if "|" in line:

                if current_commit:
                    commits.append(current_commit)

                commit_hash, author, date, message = line.split(
                    "|",
                    maxsplit=3,
                )

                current_commit = {
                    "hash": commit_hash,
                    "author": author,
                    "date": datetime.fromisoformat(date),
                    "message": message,
                    "files": [],
                }

            else:

                if current_commit:
                    current_commit["files"].append(line)

        if current_commit:
            commits.append(current_commit)

        return commits