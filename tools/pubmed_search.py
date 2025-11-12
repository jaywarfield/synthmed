# pubmed_search.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
import requests

@tool
def pubmed_search(query: str) -> str:
  """
  Search the pubmed repo.
  """

  url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
  params = {
    "db": "pubmed",
    "term": query,
    "retmode": "json",
    "retmax": 5
  }

  response = requests.get(url, params=params)
  ids = response.json()["esearchresult"]["idlist"]
  return f"PubMed IDs: {', '.join(ids)}"
