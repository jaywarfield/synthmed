# pubmed_search.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def pubmed_search(query: str) -> str:
  """
  Search the pubmed repo.
  """

  return query
