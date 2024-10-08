import asyncio
import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFMinerLoader
from pydantic.types import Path
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import Optional
import chromadb

from pdf_search.config import config


class EmbeddingService:
    @staticmethod
    async def generate_embeddings_from_pdf(
        pdf_source_path: Path,
        pdf_name: Path,
        chunk_size=4000,
        chunk_overlap=200,
        collection_name="pdf_embeddings",
    ) -> list[str]:
        """
        Generates embeddings from a PDF file and adds them to the collection.
        Returns the ids of the added embeddings.

        The PDF is first loaded, then split into chunks, and finally embedded.
        """
        loader = PDFMinerLoader(file_path=pdf_source_path)
        documents = await loader.aload()

        for doc in documents:  # associating relevant metadata with the docs
            doc.metadata["name"] = pdf_name.name
            doc.metadata["source"] = pdf_source_path.stem  # uuid without extension

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        texts = await asyncio.to_thread(text_splitter.split_documents, documents)

        embedding = GoogleGenerativeAIEmbeddings(model=config.ai.embedding_model_name)
        vectordb = Chroma(
            client=chromadb.HttpClient(
                host=config.chroma.host,
                port=config.chroma.port,
            ),
            collection_name=collection_name,
            embedding_function=embedding,
        )

        added_text_ids = await vectordb.aadd_documents(documents=texts)
        return added_text_ids

    @staticmethod
    async def delete_embeddings_of_pdf(
        pdf_uuid: uuid.UUID,
        collection_name="pdf_embeddings",
    ) -> bool:
        """
        Deletes all embeddings of a document with the given uuid from the collection.

        Returns True if all embeddings were deleted, False otherwise.
        """
        vectordb = Chroma(
            client=chromadb.HttpClient(
                host=config.chroma.host,
                port=config.chroma.port,
            ),
            collection_name=collection_name,
        )

        # Getting the ids to validate the deletion because is_deleted is never True
        # as I had to tinker with the vectordb.delete method to make it work
        #
        # For some reason, the lib takes in kwargs but doesn't use them,
        # and these kwargs are the where and where_document clauses, which are necessary
        # to delete the records in this use case.
        #
        # TURNS OUT THE 'DEPRECATED' Chroma IMPORTED FROM langchain_community.vectorstores
        # HAS THE CORRECT METHOD SIGNATURE, BUT THE 'NEW' Chroma IMPORTED FROM langchain_chroma
        # DOES NOT. WHYYYY
        ids_to_delete = vectordb.get(where={"source": str(pdf_uuid)}, include=[])["ids"]
        num_ids_to_delete = len(ids_to_delete)
        print(f"Records to delete: {num_ids_to_delete}")

        await vectordb.adelete(where={"source": str(pdf_uuid)})

        remaining_docs = vectordb.get(where={"source": str(pdf_uuid)})["ids"]
        return len(remaining_docs) == 0

    @staticmethod
    async def get_metadata(
        collection_name="pdf_embeddings",
        pdf_uuid: Optional[uuid.UUID] = None,
    ) -> list[dict]:
        """
        Fetches metadata of documents in the collection.

        - If pdf_uuid is provided, fetches metadata of the document with that uuid.
        - Otherwise, fetches metadata of all documents in the collection.
        """
        vectordb = Chroma(
            client=chromadb.HttpClient(
                host=config.chroma.host,
                port=config.chroma.port,
            ),
            collection_name=collection_name,
        )

        if pdf_uuid:
            where = {"source": str(pdf_uuid)}
            metadatas = vectordb.get(include=["metadatas"], where=where)["metadatas"]
        else:
            metadatas = vectordb.get(include=["metadatas"])["metadatas"]

        return map(dict, set(tuple(meta.items()) for meta in metadatas))
