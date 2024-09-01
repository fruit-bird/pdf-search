from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFMinerLoader

from pdf_search.config import config


class EmbeddingService:
    @staticmethod
    async def generate_embeddings_from_pdf(
        pdf_path: str,
        chunk_size=1000,
        chunk_overlap=200,
        collection_name="pdf_embeddings",
    ) -> int:
        loader = PDFMinerLoader(file_path=pdf_path)
        documents = loader.load()

        for doc in documents:  # associating relevant metadata with the docs
            doc.metadata["source"] = pdf_path

        text_spplitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        texts = text_spplitter.split_documents(documents)

        embedding = OllamaEmbeddings(model=config.ai.embedding_model_name)
        _vectordb = Chroma.from_documents(
            collection_name=collection_name,
            documents=texts,
            embedding=embedding,
            persist_directory=config.ai.embeddings_persist_path,
        )

        return len(texts)  # number of documents
