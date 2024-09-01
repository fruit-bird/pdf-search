import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain import hub
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms.ollama import Ollama


embedding = OllamaEmbeddings(model="llama3.1")
vectordb = Chroma(persist_directory="chroma-db", embedding_function=embedding)

retriever = vectordb.as_retriever()
# print(len(docs))
# print(docs[0])


def format_docs(docs: list[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def qa_chain_with_sources(question: str):
    docs = retriever.get_relevant_documents(question)

    prompt = hub.pull("rlm/rag-prompt")
    llm = Ollama(model="llama3.1")

    qa_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = qa_chain.invoke(question)
    sources = [
        f"Source {i + 1}: {doc.metadata.get('source', 'Unknown')}"
        for i, doc in enumerate(docs)
    ]
    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }


resp = qa_chain_with_sources("how do you lose in monopoly?")
print(json.dumps(resp))
