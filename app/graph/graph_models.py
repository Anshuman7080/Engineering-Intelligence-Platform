from enum import Enum


class NodeType(str, Enum):

    REPOSITORY = "Repository"

    DIRECTORY = "Directory"

    FILE = "File"

    CLASS = "Class"

    FUNCTION = "Function"

    METHOD = "Method"

    MODULE = "Module"


class RelationshipType(str, Enum):

    CONTAINS = "CONTAINS"

    DECLARES = "DECLARES"

    IMPORTS = "IMPORTS"

    CALLS = "CALLS"

    DEPENDS_ON = "DEPENDS_ON"