from fastapi import APIRouter
from pydantic.types import UUID4, List

from pdf_search.services import EmbeddingService
from pdf_search.schemas import UploadPDFResponse


router = APIRouter(prefix="/metadata", tags=["metadata"])


@router.get("/")
async def get_metadata() -> List[UploadPDFResponse]:
    return await EmbeddingService.get_metadata()


@router.get("/{pdf_source_uuid}")
async def get_metadata_about_pdf(pdf_source_uuid: UUID4) -> List[UploadPDFResponse]:
    return await EmbeddingService.get_metadata(pdf_uuid=pdf_source_uuid)
