from enum import Enum


class NodeType(str, Enum):

    REPOSITORY = "Repository"

    DIRECTORY = "Directory"

    FILE = "File"

    CLASS = "Class"

    FUNCTION = "Function"

    METHOD = "Method"

    MODULE = "Module"

    COMMIT="Commit"

    PULLREQUEST="PullRequest"

    ISSUE="Issue"

class RelationshipType(str, Enum):

    CONTAINS = "CONTAINS"

    DECLARES = "DECLARES"

    IMPORTS = "IMPORTS"

    CALLS = "CALLS"

    DEPENDS_ON = "DEPENDS_ON"

    MODIFIES="MODIFIES"

    FIXES = "FIXES"

    BELONGS_TO="BELONGS_TO"

    CREATED_BY="CREATED_BY"