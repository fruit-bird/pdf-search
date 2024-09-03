from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pdf_search.config import config
from pdf_search.routes import pdf_router, ask_router, metadata_router

app = FastAPI()
app.include_router(pdf_router)
app.include_router(ask_router)
app.include_router(metadata_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/config")
async def configuration():
    return config


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config.api.host, port=config.api.port)
