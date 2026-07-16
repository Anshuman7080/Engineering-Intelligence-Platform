from app.tools.graph_tool import GraphTool
from app.tools.vector_tool import VectorTool
from app.agents.tool_type import ToolType


class ToolRegistry:

    def __init__(self):

        self.graph_tool = GraphTool()
        self.vector_tool = VectorTool()

    def get_tool(
        self,
        tool_type: ToolType,
    ):

        if tool_type == ToolType.GRAPH:
            return self.graph_tool

        elif tool_type == ToolType.VECTOR:
            return self.vector_tool

        raise ValueError(
            f"Unsupported tool: {tool_type}"
        )