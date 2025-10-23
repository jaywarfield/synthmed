#example.py 
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool("example")
def example() -> str:
    """
    This is an example tool.   
    """

    response = "This is an example tool."
    return response
