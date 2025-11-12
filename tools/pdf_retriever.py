# pdf_retriever.py
import os
import json
from typing import Dict, List, Any
import pymupdf  # PyMuPDF
from ibm_watsonx_orchestrate.agent_builder.tools import tool

def extract_pdf_text(pdf_path: str) -> Dict[str, Any]:
    """
    Extract text, metadata, and structured content from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Dictionary containing extracted content with keys:
        - text: Full text content
        - metadata: PDF metadata (title, author, etc.)
        - pages: List of page contents
        - tables: Extracted table data (if any)
    """
    if not os.path.exists(pdf_path):
        return {"error": f"PDF file not found: {pdf_path}"}

    try:
        doc = pymupdf.open(pdf_path)

        # Extract metadata
        metadata = doc.metadata

        # Extract text from all pages
        full_text = ""
        pages = []
        tables = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text()
            full_text += page_text + "\n\n"

            pages.append({
                "page_number": page_num + 1,
                "text": page_text,
                "word_count": len(page_text.split())
            })

            # Extract tables (simple detection based on tab-separated content)
            # More sophisticated table extraction can be added later
            lines = page_text.split('\n')
            table_lines = [line for line in lines if '\t' in line and len(line.split('\t')) > 2]
            if table_lines:
                tables.append({
                    "page": page_num + 1,
                    "rows": table_lines
                })

        doc.close()

        return {
            "text": full_text.strip(),
            "metadata": metadata,
            "page_count": len(pages),
            "pages": pages,
            "tables": tables,
            "word_count": len(full_text.split())
        }

    except Exception as e:
        return {"error": f"Error processing PDF: {str(e)}"}


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
    """
    Split text into overlapping chunks for embedding and retrieval.

    Args:
        text: Input text to chunk
        chunk_size: Target size of each chunk in characters
        overlap: Number of characters to overlap between chunks

    Returns:
        List of dictionaries with chunk text and metadata
    """
    words = text.split()
    chunks = []

    # Calculate approximate words per chunk
    chars_per_word = len(text) / len(words) if words else 1
    words_per_chunk = int(chunk_size / chars_per_word)
    words_overlap = int(overlap / chars_per_word)

    start = 0
    chunk_id = 0

    while start < len(words):
        end = min(start + words_per_chunk, len(words))
        chunk_text = ' '.join(words[start:end])

        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text,
            "start_word": start,
            "end_word": end,
            "char_count": len(chunk_text),
            "word_count": end - start
        })

        chunk_id += 1
        start += words_per_chunk - words_overlap

        # Avoid very small last chunks
        if len(words) - start < words_overlap:
            break

    return chunks


@tool
def pdf_retriever(pdf_path: str, include_chunks: bool = False, chunk_size: int = 1000) -> str:
    """
    Retrieve and extract content from PDF files with optional text chunking.

    Args:
        pdf_path: Path to the PDF file (relative or absolute)
        include_chunks: Whether to include chunked text for embeddings
        chunk_size: Size of text chunks in characters (default: 1000)

    Returns:
        JSON string containing extracted PDF content including text, metadata,
        pages, tables, and optionally text chunks for RAG systems.
    """
    # Handle relative paths from knowledge_bases directory
    if not os.path.isabs(pdf_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_path = os.path.join(base_dir, pdf_path)

    # Extract PDF content
    result = extract_pdf_text(pdf_path)

    if "error" not in result and include_chunks:
        # Add chunked text for RAG/embedding purposes
        result["chunks"] = chunk_text(result["text"], chunk_size=chunk_size)

    return json.dumps(result, indent=2)
