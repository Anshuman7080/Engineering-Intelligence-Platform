from enum import Enum

class GraphQueryType(str, Enum):

    FIND_SYMBOL = "find_symbol"

    FIND_CALLERS = "find_callers"

    FIND_CALLEES = "find_callees"

    FIND_DEPENDENCIES = "find_dependencies"

    FIND_IMPORTERS = "find_importers"

    FIND_COMMITS_FOR_FILE = "find_commits_for_file"

    FIND_FILES_FOR_COMMIT = "find_files_for_commit"

    FIND_ISSUE_COMMITS = "find_issue_commits"

    FIND_ISSUE_CHANGES = "find_issue_changes"