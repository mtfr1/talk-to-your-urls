import pytest
from app.rag import RagPipeline


@pytest.mark.asyncio
async def test_index_url(monkeypatch):
    pipeline = RagPipeline()
    test_url = "http://example.com"
    fake_page_content = "Fake page content for testing."

    # Monkey-patch simple_parser to immediately return the fake content
    monkeypatch.setattr("app.rag.simple_parser", lambda _: fake_page_content)

    # Override text_splitter.split_text to return two splits
    pipeline.text_splitter.split_text = lambda text: [text[:20], text[20:]]

    # Capture the call to vector_store.aadd_documents
    aadd_called = False

    async def fake_aadd_documents(documents, ids):
        nonlocal aadd_called
        aadd_called = True
        # Ensure the correct number of documents are passed
        assert len(documents) == 2
        for doc in documents:
            # Each document should have metadata with the correct URL
            assert doc.metadata["url"] == test_url
        # Ensure ids length matches documents length
        assert len(ids) == len(documents)
        return

    monkeypatch.setattr(pipeline.vector_store, "aadd_documents", fake_aadd_documents)

    await pipeline.index_url(test_url)
    assert aadd_called