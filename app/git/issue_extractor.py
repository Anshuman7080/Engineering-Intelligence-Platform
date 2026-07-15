import re


class IssueExtractor:

    ISSUE_PATTERN = re.compile(
        r"#(\d+)"
    )

    def extract(
        self,
        message: str,
    ) -> list[str]:

        return self.ISSUE_PATTERN.findall(
            message
        )