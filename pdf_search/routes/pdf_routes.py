from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException

# from fastapi.responses import FileResponse
from pydantic.types import UUID4

from pdf_search.services import PDFService, EmbeddingService, QAService
from pdf_search.schemas import (
    UploadPDFResponse,
    AskQuestionRequest,
    AskQuestionResponse,
    DeletePDFResponse,
)


router = APIRouter(prefix="/pdf", tags=["pdf"])


# https://restfulapi.net/rest-api-design-for-long-running-tasks/
@router.post("/", status_code=202)
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
) -> UploadPDFResponse:
    # - [x] upload pdf to s3, now only to bucket/ directory
    # - [x] extract text from pdf
    #   - [x] generate embeddings from text
    #   - [x] store embeddings in chroma
    # - [x] return success message + metadata (e.g. s3 url, uuid of pdf, etc.)

    upload_name, source = await PDFService.upload_pdf(file)
    # background tasks cannot be checked for completion,
    # and answers online suggest using a lib called Celery, which seems overkill,
    # although checking for completion in a real environment is neccessary
    background_tasks.add_task(
        EmbeddingService.generate_embeddings_from_pdf,
        pdf_source_path=source,
        pdf_name=upload_name,
    )

    return UploadPDFResponse(
        name=upload_name.name,
        source=source.stem,
    )


@router.delete("/{uuid}")
async def delete_pdf(uuid: UUID4) -> None:
    is_deleted = await EmbeddingService.delete_embeddings_of_pdf(uuid)
    if not is_deleted:
        raise HTTPException(status_code=500, detail="Failed to delete embeddings")

    await PDFService.delete_pdf(uuid)
    return DeletePDFResponse()


@router.post("/ask")
async def ask_question(req: AskQuestionRequest) -> AskQuestionResponse:
    return await QAService.ask_question(question=req.question)


@router.post("/ask/{pdf_source_uuid}")
async def ask_question_about_pdf(
    req: AskQuestionRequest,
    pdf_source_uuid: UUID4,
) -> AskQuestionResponse:
    return await QAService.ask_question(
        question=req.question,
        metadata_filter={"source": str(pdf_source_uuid)},
    )


@router.get("/metadata")
async def get_metadata() -> list[dict]:
    return await EmbeddingService.get_all_metadata()
