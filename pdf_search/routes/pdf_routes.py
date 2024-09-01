from fastapi import APIRouter, UploadFile, File
from pydantic.types import UUID4

from pdf_search.services import PDFService, EmbeddingService, QAService
from pdf_search.schemas import (
    UploadPDFResponse,
    AskQuestionRequest,
    AskQuestionResponse,
)


router = APIRouter(prefix="/pdf", tags=["pdf"])


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)) -> UploadPDFResponse:
    # - [x] upload pdf to s3, now only to bucket/ directory
    # - [x] extract text from pdf
    #   - [x] generate embeddings from text
    #   - [x] store embeddings in chroma
    # - [x] return success message + metadata (e.g. s3 url, uuid of pdf, etc.)

    uuid, file_storage_path = await PDFService.upload_pdf(file)
    num_documents = await EmbeddingService.generate_embeddings_from_pdf(
        pdf_path=file_storage_path
    )

    return {
        "file": {
            "uuid": uuid,
            "location": file_storage_path,
            "size_bytes": file.size,
        },
        "embeddings": {"num_documents": num_documents},
        "message": "File uploaded successfully and embeddings generated",
    }


@router.post("/ask")
async def ask_question(req: AskQuestionRequest) -> AskQuestionResponse:
    return await QAService.ask_question(question=req.question)
