from uuid import uuid4

import httpx
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings
from app.utils import format_docs, simple_parser


class RagPipeline:
    def __init__(self) -> None:
        """Initializes the RAG pipeline with the necessary components."""

        self.embedder = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004", google_api_key=settings.GOOGLE_API_KEY
        )

        self.llm = GoogleGenerativeAI(
            model="gemini-2.0-flash-lite", api_key=settings.GOOGLE_API_KEY
        )

        self.vector_store = Chroma(
            collection_name="url_indexer",
            embedding_function=self.embedder,
            persist_directory="./data/chromadb/",
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )

    @staticmethod
    async def _get_url_html(url: str) -> bytes:
        async with httpx.AsyncClient(verify=False, timeout=30) as client:
            try:
                r = await client.get(url=url)
                r.raise_for_status()
                return r.content
            except httpx.HTTPStatusError as e:
                raise httpx.HTTPStatusError(f"Failed to fetch URL: {e}")

    async def index_url(self, url: str) -> None:
        """Indexes the content of a given URL.

           Fetches the URL content through an HTTP GET request, processes the content
           by splitting it into smaller chunks, and adding these chunks as documents
           to a vector store.

        Args:
            url (str): The URL of the page to be indexed.
        """

        html_content = await self._get_url_html(url)

        page_content = simple_parser(html_content)

        splits = self.text_splitter.split_text(page_content)

        documents = [
            Document(page_content=split, metadata={"url": url}) for split in splits
        ]

        ids = [str(uuid4()) for _ in range(len(splits))]

        await self.vector_store.aadd_documents(
            documents=documents,
            ids=ids,
        )

    async def ask_question(
        self, question: str, url: str, chat_history: list[BaseMessage] = None
    ) -> str:
        """Asynchronously answers a question based on a specific URL's context.

        Args:
            question (str): The question to be answered.
            url (str): The URL used to filter the context from the vector store.
            chat_history (list[BaseMessage], optional): A list of chat history messages.
                Defaults to None.

        Returns:
            str: A concise answer to the question based on the retrieved context.

        Notes:
            - If the answer cannot be determined from the context, the response will indicate
              that the answer is unknown.
            - The answer is limited to three sentences for brevity.
        """
        retriever = self.vector_store.as_retriever(
            search_kwargs={"filter": {"url": url}}
        )

        template = """
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know because you
        don't have enough context, don't try to make up an answer.
        Use three sentences maximum and keep the answer as concise as possible.

        {context}

        {chat_history}

        Question: {question}

        Helpful Answer:
        """

        prompt = PromptTemplate.from_template(
            template, partial_variables={"chat_history": chat_history}
        )

        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return await chain.ainvoke(question)
