from app.utils import simple_parser, format_docs
from langchain_core.documents import Document

def test_simple_parser():
    html = b"""
        <html>
            <head>
                <style>body {color: red;}</style>
                <script>console.log('test');</script>
            </head>
            <body>
                <h1>Title</h1>
                <p>Some text</p>
            </body>
        </html>
    """
    result = simple_parser(html)
    assert result == "Title Some text"


def test_format_docs():
    docs = [
        Document(page_content="First document"),
        Document(page_content="Second document"),
        Document(page_content="Third document")
    ]
    result = format_docs(docs)
    assert result == "First document\n\nSecond document\n\nThird document"
