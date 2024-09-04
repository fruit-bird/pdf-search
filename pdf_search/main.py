import os
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from pdf_search.config import config
from pdf_search.routes import pdf_router, ask_router, metadata_router

os.makedirs(config.api.pdf_storage_path, exist_ok=True)
os.environ["GOOGLE_API_KEY"] = config.ai.google_api_key


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(pdf_router)
v1_router.include_router(ask_router)
v1_router.include_router(metadata_router)

app = FastAPI()
app.include_router(v1_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.api.url()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@v1_router.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config.api.host, port=config.api.port)
