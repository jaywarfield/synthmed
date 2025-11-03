#test1.py 
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool("test1")
def test1() -> str:
    """
    This is the test1 tool.   
    """

    response = "This is the test1 tool."
    return response
