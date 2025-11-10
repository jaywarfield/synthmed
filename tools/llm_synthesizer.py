# llm_synthesizer.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def llm_synthesizer(query: str) -> str:
  """
  Synthesize the LLM.
  """

  return query
