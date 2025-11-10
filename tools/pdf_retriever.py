# pdf_retriever.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def pdf_retriever(query: str) -> str:
  """
  Retrieve the pdfs.
  """

  return query
