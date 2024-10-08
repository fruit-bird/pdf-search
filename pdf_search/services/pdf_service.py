import os
import uuid
import aiofiles
from pathlib import Path as PathlibPath
from fastapi import UploadFile, HTTPException, File
from pydantic.types import Path

from pdf_search.config import config


class PDFService:
    @staticmethod
    async def upload_pdf(
        file: UploadFile = File(...),
        file_uuid: uuid.UUID = None,  # used for updating existing files
    ) -> tuple[Path, Path]:
        """
        Uploads a single PDF file to the configured storage location.

        File are rename to UUIDs to prevent collisions.
        The new filename is returned in the response.

        Returns a tuple containing the uuid and the storage path of the uploaded file.
        """
        uuid_val = file_uuid or uuid.uuid4()
        filename = f"{uuid_val}.pdf"

        # if file.content_type != "application/pdf":  # should perform better validation
        #     raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        file_storage_path = os.path.join(config.api.pdf_storage_path, filename)

        try:
            async with aiofiles.open(file_storage_path, "wb") as f:
                content = await file.read()
                await f.write(content)
        except Exception as _:
            raise HTTPException(status_code=500, detail="File could not be saved")

        upload_name = Path(file.filename)
        source = Path(file_storage_path)

        return upload_name, source

    @staticmethod
    async def delete_pdf(uuid: uuid.UUID):
        """
        Deletes a PDF file from the configured storage location.
        """
        file_path = os.path.join(config.api.pdf_storage_path, f"{uuid}.pdf")
        try:
            os.remove(file_path)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="File not found")
        except Exception as _:
            raise HTTPException(status_code=500, detail="File could not be deleted")

    @staticmethod
    async def download_pdf(file_uuid: uuid.UUID) -> str:
        pdf_path = [
            f
            for f in os.listdir(config.api.pdf_storage_path)
            if PathlibPath(f).stem == str(file_uuid)
        ]

        print(pdf_path)
        if len(pdf_path) != 1:
            raise HTTPException(status_code=404, detail="File not found")

        pdf_path = os.path.join(config.api.pdf_storage_path, pdf_path[0])
        return pdf_path
