from app.retrieval.retriever import Retriever
from app.tools.tool_response import ToolResponse

class VectorTool:

    def __init__(self):

        self.retriever = Retriever()

    def execute(
        self,
        query: str,
        user_id:str,
        repository_name: str,
        top_k: int = 5,
    ):

        results= self.retriever.search(
            query=query,
            user_id=user_id,
            repository_name=repository_name,
            top_k=top_k,
        )

        return ToolResponse(
            tool="vector",
            query_type="semantic_search",
            results=results,
        )