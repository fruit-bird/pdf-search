from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pydantic.types import UUID4

from pdf_search.services import PDFService, EmbeddingService
from pdf_search.schemas import (
    UploadPDFResponse,
    DeletePDFResponse,
)


router = APIRouter(prefix="/pdf", tags=["pdf"])


# https://restfulapi.net/rest-api-design-for-long-running-tasks/
@router.post("/")
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
    # background_tasks.add_task(
    #     EmbeddingService.generate_embeddings_from_pdf,
    #     pdf_source_path=source,
    #     pdf_name=upload_name,
    # )
    await EmbeddingService.generate_embeddings_from_pdf(
        pdf_source_path=source,
        pdf_name=upload_name,
    )

    return UploadPDFResponse(
        name=upload_name.name,
        source=source.stem,
    )


@router.delete("/{uuid}")
async def delete_pdf(uuid: UUID4) -> DeletePDFResponse:
    is_deleted = await EmbeddingService.delete_embeddings_of_pdf(uuid)
    if not is_deleted:
        raise HTTPException(status_code=500, detail="Failed to delete embeddings")

    await PDFService.delete_pdf(uuid)
    return DeletePDFResponse()


@router.get("/{uuid}")
async def download_pdf(uuid: UUID4) -> FileResponse:
    pdf_path = await PDFService.download_pdf(uuid)
    return FileResponse(pdf_path)


@router.put("/{uuid}", status_code=202)
async def update_pdf(
    uuid: UUID4,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
) -> UploadPDFResponse:
    # FIRST DELETE OLD EMBEDDINGS AND PDF
    is_deleted = await EmbeddingService.delete_embeddings_of_pdf(uuid)
    if not is_deleted:
        raise HTTPException(status_code=500, detail="Failed to delete old embeddings")

    await PDFService.delete_pdf(uuid)

    upload_name, source = await PDFService.upload_pdf(file, file_uuid=uuid)
    # background tasks cannot be checked for completion,
    # and answers online suggest using a lib called Celery, which seems overkill,
    # although checking for completion in a real environment is neccessary
    await EmbeddingService.generate_embeddings_from_pdf(
        pdf_source_path=source,
        pdf_name=upload_name,
    )

    return UploadPDFResponse(
        name=upload_name.name,
        source=source.stem,
    )
