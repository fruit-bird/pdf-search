from pydantic import BaseModel
from pydantic.types import Path, List


class UploadPDFResponse(BaseModel):
    name: Path  # upload name (original_name.pdf)
    source: Path  # storage pdf name without ext (uuid~~.pdf~~)


class AskQuestionRequest(BaseModel):
    question: str


class AskQuestionResponse(BaseModel):
    question: str
    answer: str
    sources: List[Path]
    names: List[str]


class DeletePDFResponse(BaseModel):
    message: str = "PDF deleted successfully"
