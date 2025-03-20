from fastapi import APIRouter, HTTPException, status

from app.rag import RagPipeline
from app.schemas import AskRequest, AskResponse, IndexURLRequest, IndexURLResponse
from app.utils import get_url_document_ids

router = APIRouter()

rag_pipeline = RagPipeline()


@router.post("/index-url", status_code=status.HTTP_201_CREATED)
async def index_url(request: IndexURLRequest) -> IndexURLResponse:
    """Index a URL for future question answering."""
    document_ids = get_url_document_ids(
        vector_store=rag_pipeline.vector_store, url=request.url, limit=1
    )
    if len(document_ids) > 0:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail=f"URL {request.url} was already indexed"
        )

    try:
        await rag_pipeline.index_url(request.url)
        return {"message": f"URL {request.url} indexed successfully"}
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/delete-url", status_code=status.HTTP_200_OK)
async def delete_url(request: IndexURLRequest) -> IndexURLResponse:
    """Endpoint for deleting an already indexed URL"""
    document_ids = get_url_document_ids(
        vector_store=rag_pipeline.vector_store, url=request.url
    )
    if len(document_ids) > 0:
        rag_pipeline.vector_store.delete(document_ids)
        return {"message": f"Documents with URL: {request.url} sucessfully deleted"}
    raise HTTPException(
        status.HTTP_404_NOT_FOUND, detail=f"URL {request.url} is not indexed."
    )


@router.post("/ask", status_code=status.HTTP_200_OK)
async def ask(ask: AskRequest) -> AskResponse:
    """Ask a question to the RAG model."""
    try:
        llm_answer = await rag_pipeline.ask_question(question=ask.question, url=ask.url)
        return {"answer": llm_answer}
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
