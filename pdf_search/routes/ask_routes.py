from fastapi import APIRouter
from pydantic.types import UUID4

from pdf_search.services import QAService
from pdf_search.schemas import (
    AskQuestionRequest,
    AskQuestionResponse,
)

router = APIRouter(prefix="/ask", tags=["qa"])


@router.post("/")
async def ask_question(req: AskQuestionRequest) -> AskQuestionResponse:
    return await QAService.ask_question(question=req.question)


@router.post("/{pdf_source_uuid}")
async def ask_question_about_pdf(
    req: AskQuestionRequest,
    pdf_source_uuid: UUID4,
) -> AskQuestionResponse:
    return await QAService.ask_question(
        question=req.question,
        metadata_filter={"source": str(pdf_source_uuid)},
    )
