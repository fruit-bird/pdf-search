import os
import uuid
import aiofiles
from fastapi import UploadFile, HTTPException, File

from pdf_search.config import config


class PDFService:
    @staticmethod
    async def upload_pdf(file: UploadFile = File(...)) -> tuple[uuid.UUID, str]:
        """
        Uploads a single PDF file to the configured storage location.

        File names are prefixed with a UUID to prevent collisions.
        The new filename is returned in the response.

        Returns a tuple containing the uuid and the storage path of the uploaded file.
        """
        uuid_val = uuid.uuid4()
        filename = f"{uuid_val}_{file.filename}"

        # if file.content_type != "application/pdf":  # should perform better validation
        #     raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        file_storage_path = os.path.join(config.api.pdf_storage_path, filename)

        try:
            async with aiofiles.open(file_storage_path, "wb") as f:
                content = await file.read()
                await f.write(content)
        except Exception as _:
            raise HTTPException(status_code=500, detail="File could not be saved")

        return uuid_val, file_storage_path
