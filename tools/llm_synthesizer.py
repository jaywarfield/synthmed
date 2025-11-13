# llm_synthesizer.py

import os
import json
from typing import List, Dict, Any, Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool


class MedicalSynthesizer:
    """
    Medical research synthesizer using IBM watsonx.ai.
    """

    def __init__(self, model_id: str = "meta-llama/llama-3-2-90b-vision-instruct"):
        """
        Initialize the synthesizer.

        Args:
            model_id: IBM watsonx.ai model ID to use
        """
        self.model_id = model_id

        # Try to import IBM watsonx.ai SDK
        try:
            from ibm_watsonx_ai import APIClient
            from ibm_watsonx_ai import Credentials
            from ibm_watsonx_ai.foundation_models import ModelInference

            api_key = os.environ.get("WATSONX_API_KEY")
            project_id = os.environ.get("WATSONX_PROJECT_ID")

            if api_key and project_id:
                credentials = Credentials(
                    url="https://us-south.ml.cloud.ibm.com",
                    api_key=api_key
                )
                self.client = APIClient(credentials)
                self.model = ModelInference(
                    model_id=model_id,
                    credentials=credentials,
                    project_id=project_id
                )
                self.watsonx_available = True
            else:
                self.watsonx_available = False

        except ImportError:
            self.watsonx_available = False

    def synthesize_with_context(self,
                                 query: str,
                                 retrieved_passages: List[Dict[str, Any]],
                                 output_format: str = "comprehensive") -> Dict[str, Any]:
        """
        Synthesize information from multiple retrieved passages.

        Args:
            query: Research question or query
            retrieved_passages: List of relevant passages with metadata
            output_format: Output format (comprehensive, summary, table)

        Returns:
            Dictionary with synthesized content
        """
        # Build context from retrieved passages
        context = self._build_context(retrieved_passages)

        # Create synthesis prompt
        prompt = self._create_synthesis_prompt(query, context, output_format)

        # Generate synthesis
        if self.watsonx_available:
            synthesis = self._generate_with_watsonx(prompt)
        else:
            synthesis = self._generate_fallback(prompt, context)

        # Extract citations from passages
        citations = self._extract_citations(retrieved_passages)

        return {
            "query": query,
            "synthesis": synthesis,
            "citations": citations,
            "source_count": len(retrieved_passages),
            "model": self.model_id if self.watsonx_available else "fallback"
        }

    def _build_context(self, passages: List[Dict[str, Any]]) -> str:
        """
        Build context string from retrieved passages.

        Args:
            passages: List of passage dictionaries

        Returns:
            Formatted context string
        """
        context_parts = []

        for i, passage in enumerate(passages):
            text = passage.get("text", "")
            metadata = passage.get("metadata", {})

            source = metadata.get("source", "Unknown source")
            domain = metadata.get("disease_domain", "general")

            context_parts.append(
                f"[Source {i+1}: {source}, Domain: {domain}]\n{text}\n"
            )

        return "\n---\n".join(context_parts)

    def _create_synthesis_prompt(self,
                                  query: str,
                                  context: str,
                                  output_format: str) -> str:
        """
        Create synthesis prompt for the LLM.

        Args:
            query: Research question
            context: Retrieved context passages
            output_format: Desired output format

        Returns:
            Formatted prompt string
        """
        if output_format == "comprehensive":
            format_instructions = """
Generate a comprehensive research synthesis with:
1. Executive Summary (2-3 sentences)
2. Detailed Synthesis (organized by key themes)
3. Key Findings (bullet points)
4. Cross-Domain Connections (if applicable)
5. References (numbered list)
"""
        elif output_format == "summary":
            format_instructions = """
Generate a concise summary (3-5 sentences) that:
- Answers the research question directly
- Highlights the most important findings
- Maintains scientific accuracy
"""
        else:  # table
            format_instructions = """
Generate a structured table format with:
- Disease Domain | Key Finding | Source | Confidence
- Organize findings by domain
- Include citations
"""

        prompt = f"""You are a medical research synthesis expert. Analyze the following research question and context to generate a comprehensive, accurate synthesis.

Research Question:
{query}

Context from Medical Literature:
{context}

Instructions:
{format_instructions}

Requirements:
- Synthesize information across all sources
- Maintain scientific rigor and accuracy
- Use proper citations [Source X]
- Identify areas of consensus and disagreement
- Note confidence levels and evidence quality
- Avoid making clinical recommendations

Synthesis:"""

        return prompt

    def _generate_with_watsonx(self, prompt: str) -> str:
        """
        Generate synthesis using IBM watsonx.ai.

        Args:
            prompt: Input prompt

        Returns:
            Generated synthesis text
        """
        try:
            parameters = {
                "max_new_tokens": 2000,
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 50
            }

            response = self.model.generate_text(
                prompt=prompt,
                params=parameters
            )

            return response

        except Exception as e:
            return f"Error generating with watsonx.ai: {str(e)}"

    def _generate_fallback(self, prompt: str, context: str) -> str:
        """
        Fallback synthesis when watsonx.ai is not available.

        Args:
            prompt: Input prompt
            context: Retrieved context

        Returns:
            Basic synthesis based on context
        """
        # Extract key information from context
        sources = context.split("---")

        synthesis = "## Synthesis (Fallback Mode - IBM watsonx.ai not configured)\n\n"
        synthesis += "**Note:** This is a basic extraction. For AI-powered synthesis, configure IBM watsonx.ai credentials.\n\n"

        synthesis += f"### Retrieved Sources ({len(sources)})\n\n"
        for i, source in enumerate(sources[:5]):  # Limit to first 5
            lines = source.strip().split('\n')
            if len(lines) > 2:
                synthesis += f"{i+1}. {lines[0]}\n"
                synthesis += f"   Preview: {lines[1][:200]}...\n\n"

        synthesis += "\n### Action Required\n"
        synthesis += "Configure IBM watsonx.ai to enable AI-powered synthesis:\n"
        synthesis += "1. Set WATSONX_API_KEY environment variable\n"
        synthesis += "2. Set WATSONX_PROJECT_ID environment variable\n"

        return synthesis

    def _extract_citations(self, passages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Extract citations from retrieved passages.

        Args:
            passages: List of passage dictionaries

        Returns:
            List of citation dictionaries
        """
        citations = []

        for i, passage in enumerate(passages):
            metadata = passage.get("metadata", {})

            citation = {
                "id": i + 1,
                "source": metadata.get("source", "Unknown"),
                "title": metadata.get("title", "Unknown"),
                "author": metadata.get("author", "Unknown"),
                "disease_domain": metadata.get("disease_domain", "general"),
                "url": metadata.get("pdf_path", "")
            }

            citations.append(citation)

        return citations

    def synthesize_cross_domain(self,
                                query: str,
                                domain_results: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Synthesize information across multiple disease domains.

        Args:
            query: Research question
            domain_results: Dictionary mapping domains to retrieved passages

        Returns:
            Cross-domain synthesis
        """
        # Combine all passages
        all_passages = []
        domain_summary = {}

        for domain, passages in domain_results.items():
            all_passages.extend(passages)
            domain_summary[domain] = len(passages)

        # Generate synthesis
        synthesis = self.synthesize_with_context(query, all_passages, "comprehensive")

        # Add domain breakdown
        synthesis["domain_breakdown"] = domain_summary

        return synthesis


# Tool wrappers for IBM watsonx Orchestrate
@tool
def llm_synthesizer(query: str, context: str, output_format: str = "comprehensive") -> str:
    """
    Synthesize medical research information using IBM watsonx.ai LLM.

    Args:
        query: Research question to answer
        context: Retrieved context passages (JSON string or plain text)
        output_format: Output format (comprehensive, summary, or table)

    Returns:
        JSON string with synthesized content, citations, and metadata
    """
    synthesizer = MedicalSynthesizer()

    # Parse context if it's JSON
    try:
        passages = json.loads(context)
        if not isinstance(passages, list):
            passages = [{"text": context, "metadata": {}}]
    except json.JSONDecodeError:
        passages = [{"text": context, "metadata": {}}]

    result = synthesizer.synthesize_with_context(query, passages, output_format)

    return json.dumps(result, indent=2)


@tool
def synthesize_research_query(query: str,
                               knowledge_base_results: str,
                               pubmed_results: str = None) -> str:
    """
    Synthesize information from both local knowledge base and PubMed sources.

    Args:
        query: Research question
        knowledge_base_results: JSON string with RAG retrieval results
        pubmed_results: Optional JSON string with PubMed search results

    Returns:
        JSON string with comprehensive synthesis combining all sources
    """
    synthesizer = MedicalSynthesizer()

    # Parse knowledge base results
    kb_passages = json.loads(knowledge_base_results) if knowledge_base_results else []

    # Parse PubMed results if provided
    if pubmed_results:
        try:
            pubmed_data = json.loads(pubmed_results)
            articles = pubmed_data.get("articles", [])

            # Convert PubMed articles to passage format
            for article in articles:
                kb_passages.append({
                    "text": f"{article['title']}\n\n{article['abstract']}",
                    "metadata": {
                        "source": f"PubMed: {article['pmid']}",
                        "title": article['title'],
                        "author": ", ".join(article.get('authors', [])[:3]),
                        "disease_domain": "pubmed",
                        "citation": article.get('citation', ''),
                        "url": article.get('url', '')
                    }
                })
        except json.JSONDecodeError:
            pass

    # Generate synthesis
    result = synthesizer.synthesize_with_context(query, kb_passages, "comprehensive")

    return json.dumps(result, indent=2)

