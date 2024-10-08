from langchain_chroma.vectorstores import Chroma
from langchain import hub
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import chromadb

from pdf_search.config import config
from pdf_search.schemas import AskQuestionResponse


def format_docs(docs: list[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


class QAService:
    @staticmethod
    async def ask_question(
        question: str,
        collection_name: str = "pdf_embeddings",
        metadata_filter: dict = None,
    ) -> AskQuestionResponse:
        """
        Ask a question and return the answer with the relevant sources.

        - If `metadata_filter` is provided, it will be used to query only the documents that match the filter.
        - Otherwise, all documents will be queried.
        """
        embedding = GoogleGenerativeAIEmbeddings(model=config.ai.embedding_model_name)
        vectordb = Chroma(
            client=chromadb.HttpClient(
                host=config.chroma.host,
                port=config.chroma.port,
            ),
            collection_name=collection_name,
            embedding_function=embedding,
        )

        retriever = vectordb.as_retriever(search_kwargs={"filter": metadata_filter})

        prompt = hub.pull("rlm/rag-prompt")
        llm = GoogleGenerativeAI(model=config.ai.model_name)

        qa_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )

        answer = await qa_chain.ainvoke(question)
        docs = await retriever.ainvoke(question)
        sources = [doc.metadata.get("source", "Unknown") for doc in docs]
        names = [doc.metadata.get("name", "Unknown") for doc in docs]

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "names": names,
        }
