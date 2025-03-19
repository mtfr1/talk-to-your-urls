from pydantic import BaseModel


class IndexURLRequest(BaseModel):
    url: str


class IndexURLResponse(BaseModel):
    message: str


class AskRequest(BaseModel):
    question: str
    url: str


class AskResponse(BaseModel):
    answer: str
