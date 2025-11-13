# pubmed_search.py


import json
import time
from typing import Dict, List, Any, Optional
import requests
from xml.etree import ElementTree as ET
from ibm_watsonx_orchestrate.agent_builder.tools import tool


class PubMedSearcher:
    """
    PubMed API client for searching medical literature.
    """

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    def __init__(self, email: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize PubMed searcher.

        Args:
            email: Email for NCBI (recommended for higher rate limits)
            api_key: NCBI API key (optional, for higher rate limits)
        """
        self.email = email or "synthmed@example.com"
        self.api_key = api_key
        self.session = requests.Session()

    def search(self, query: str, max_results: int = 10, sort: str = "relevance") -> List[str]:
        """
        Search PubMed for articles matching the query.

        Args:
            query: Search query
            max_results: Maximum number of results to return
            sort: Sort order (relevance, pub_date, etc.)

        Returns:
            List of PubMed IDs (PMIDs)
        """
        url = f"{self.BASE_URL}esearch.fcgi"

        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "sort": sort,
            "email": self.email
        }

        if self.api_key:
            params["api_key"] = self.api_key

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            pmids = data.get("esearchresult", {}).get("idlist", [])

            return pmids

        except Exception as e:
            return {"error": f"PubMed search failed: {str(e)}"}

    def fetch_details(self, pmids: List[str]) -> List[Dict[str, Any]]:
        """
        Fetch detailed information for PubMed articles.

        Args:
            pmids: List of PubMed IDs

        Returns:
            List of article details with abstracts and metadata
        """
        if not pmids:
            return []

        url = f"{self.BASE_URL}efetch.fcgi"

        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
            "email": self.email
        }

        if self.api_key:
            params["api_key"] = self.api_key

        try:
            # Respect rate limits (3 requests/second without API key, 10/second with key)
            time.sleep(0.34 if not self.api_key else 0.1)

            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()

            # Parse XML response
            root = ET.fromstring(response.content)

            articles = []
            for article in root.findall(".//PubmedArticle"):
                parsed = self._parse_article(article)
                if parsed:
                    articles.append(parsed)

            return articles

        except Exception as e:
            return {"error": f"PubMed fetch failed: {str(e)}"}

    def _parse_article(self, article_xml) -> Optional[Dict[str, Any]]:
        """
        Parse article XML into structured dictionary.

        Args:
            article_xml: XML element for a PubMed article

        Returns:
            Dictionary with article details
        """
        try:
            # Extract PMID
            pmid_elem = article_xml.find(".//PMID")
            pmid = pmid_elem.text if pmid_elem is not None else "Unknown"

            # Extract title
            title_elem = article_xml.find(".//ArticleTitle")
            title = title_elem.text if title_elem is not None else "No title"

            # Extract abstract
            abstract_parts = article_xml.findall(".//Abstract/AbstractText")
            abstract = " ".join([part.text for part in abstract_parts if part.text])

            # Extract authors
            authors = []
            for author in article_xml.findall(".//Author"):
                last_name = author.find("LastName")
                fore_name = author.find("ForeName")
                if last_name is not None:
                    author_name = last_name.text
                    if fore_name is not None:
                        author_name = f"{fore_name.text} {author_name}"
                    authors.append(author_name)

            # Extract journal info
            journal_elem = article_xml.find(".//Journal/Title")
            journal = journal_elem.text if journal_elem is not None else "Unknown"

            # Extract publication date
            pub_date = article_xml.find(".//PubDate")
            year = pub_date.find("Year").text if pub_date is not None and pub_date.find("Year") is not None else "Unknown"

            # Extract DOI
            doi_elem = article_xml.find(".//ArticleId[@IdType='doi']")
            doi = doi_elem.text if doi_elem is not None else None

            return {
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "journal": journal,
                "year": year,
                "doi": doi,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "citation": self._format_citation(authors, title, journal, year)
            }

        except Exception as e:
            return None

    def _format_citation(self, authors: List[str], title: str, journal: str, year: str) -> str:
        """
        Format article citation in standard format.

        Args:
            authors: List of author names
            title: Article title
            journal: Journal name
            year: Publication year

        Returns:
            Formatted citation string
        """
        if authors:
            if len(authors) == 1:
                author_str = authors[0]
            elif len(authors) == 2:
                author_str = f"{authors[0]} and {authors[1]}"
            else:
                author_str = f"{authors[0]} et al."
        else:
            author_str = "Unknown authors"

        return f"{author_str}. {title}. {journal}. {year}."

    def search_and_fetch(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """
        Search PubMed and fetch full article details in one call.

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            Dictionary with search results and article details
        """
        # Search for PMIDs
        pmids = self.search(query, max_results=max_results)

        if isinstance(pmids, dict) and "error" in pmids:
            return pmids

        # Fetch article details
        articles = self.fetch_details(pmids)

        if isinstance(articles, dict) and "error" in articles:
            return articles

        return {
            "query": query,
            "result_count": len(articles),
            "max_results": max_results,
            "articles": articles
        }


# Tool wrapper for IBM watsonx Orchestrate
@tool
def pubmed_search(query: str, max_results: int = 10) -> str:
    """
    Search PubMed for medical research articles and retrieve abstracts.

    Args:
        query: Search query (e.g., "autism genetics", "cancer metastasis")
        max_results: Maximum number of articles to return (default: 10)

    Returns:
        JSON string containing articles with titles, abstracts, authors,
        journal information, and citations.
    """
    searcher = PubMedSearcher()
    result = searcher.search_and_fetch(query, max_results=max_results)
    return json.dumps(result, indent=2)

