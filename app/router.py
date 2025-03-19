from fastapi import APIRouter, HTTPException, status

from app.rag import RagPipeline
from app.schemas import AskRequest, AskResponse, IndexURLRequest, IndexURLResponse

router = APIRouter()

rag_pipeline = RagPipeline()


@router.post("/index-url", status_code=status.HTTP_201_CREATED)
async def index_url(request: IndexURLRequest) -> IndexURLResponse:
    """Index a URL for future question answering."""
    try:
        await rag_pipeline.index_url(request.url)
        return {"message": "URL indexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask", status_code=status.HTTP_200_OK)
async def ask(ask: AskRequest) -> AskResponse:
    """Ask a question to the RAG model."""
    try:
        llm_answer = await rag_pipeline.ask_question(question=ask.question, url=ask.url)
        return {"answer": llm_answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
