from sqlalchemy.ext.asyncio import create_async_engine

from pdf_search.config import config


async def get_db():
    db = create_async_engine(config.database.url())
    try:
        yield db
    finally:
        await db.dispose()
