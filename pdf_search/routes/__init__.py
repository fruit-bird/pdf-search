from .pdf_routes import router as pdf_router
from .ask_routes import router as ask_router
from .metadata_routes import router as metadata_router

__all__ = ["pdf_router", "ask_router", "metadata_router"]
