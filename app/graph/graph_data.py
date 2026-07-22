from dataclasses import dataclass, field


@dataclass
class GraphNode:

    label: str
    properties: dict


@dataclass
class GraphRelationship:

    start_label: str
    start_properties: dict

    end_label: str
    end_properties: dict

    relationship: str


@dataclass
class GraphData:

    nodes: list[GraphNode] = field(default_factory=list)

    relationships: list[GraphRelationship] = field(default_factory=list)

    def add_node(
        self,
        label: str,
        **properties,
    ):

        self.nodes.append(
            GraphNode(
                label=label,
                properties=properties,
            )
        )

    def add_relationship(
        self,
        start_label: str,
        start_properties: dict,
        end_label: str,
        end_properties: dict,
        relationship: str,
    ):

        self.relationships.append(
            GraphRelationship(
                start_label=start_label,
                start_properties=start_properties,
                end_label=end_label,
                end_properties=end_properties,
                relationship=relationship,
            )
        )

    def merge(
        self,
        other: "GraphData",
    ):

        self.nodes.extend(other.nodes)
        self.relationships.extend(other.relationships)