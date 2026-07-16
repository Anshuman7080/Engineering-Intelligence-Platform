from app.tools.graph_tool import GraphTool 
from app.tools.vector_tool import VectorTool
from app.agents.tool_type import ToolType


class ToolRegistry:

    def __init__(self):
        self.graph_tool = GraphTool()