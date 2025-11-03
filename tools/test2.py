#test2.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool("test2")
def tool2(input: str) -> str:
    """Executes the tool's action based on the provided input.

    Args:
        input (str): The input of the tool.

    Returns:
        str: The action of the tool.
    """

    #functionality of the tool

    return f"Hello, {input}"
