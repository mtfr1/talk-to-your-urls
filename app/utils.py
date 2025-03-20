import bs4
from langchain_core.documents import Document
from langchain_chroma import Chroma


def simple_parser(html: bytes) -> str:
    """Recursively deletes script and style HTLM tags"""
    soup = bs4.BeautifulSoup(html, "html.parser")
    for data in soup(["style", "script"]):
        data.decompose()
    return " ".join(soup.stripped_strings)


def format_docs(docs: list[Document]) -> str:
    """Joins a list of documents into a single string with linebreaks as delimiters"""
    return "\n\n".join(doc.page_content for doc in docs)


def get_url_document_ids(vector_store: Chroma, url: str, limit: int = None) -> list[str]:
    """Given a URL, returns a list of documents with this URL as metadata"""
    document_ids = vector_store.get(
        limit=limit,
        where={"url": {"$eq": url}},
    )['ids']

    return document_ids