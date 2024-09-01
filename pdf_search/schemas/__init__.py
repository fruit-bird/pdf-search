from pydantic import BaseModel
from pydantic.types import UUID4, Path


class UploadPDFResponse(BaseModel):
    class UploadPDFResponseFile(BaseModel):
        uuid: UUID4
        location: Path
        size_bytes: int

    class UploadPDFResponseEmbeddings(BaseModel):
        num_documents: int

    file: UploadPDFResponseFile
    embeddings: UploadPDFResponseEmbeddings
    message: str


class AskQuestionRequest(BaseModel):
    question: str


class AskQuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[Path]
