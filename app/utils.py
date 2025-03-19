import bs4
from langchain_core.documents import Document


def simple_parser(html: bytes) -> str:
    soup = bs4.BeautifulSoup(html, "html.parser")
    for data in soup(["style", "script"]):
        data.decompose()
    return " ".join(soup.stripped_strings)


def format_docs(docs: list[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)
