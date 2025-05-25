from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.config import app_settings, logger
from app.db.base import Base
from app.db.session import engine
from app.routes import root_router
from app.utils.fastapi_utils.builder import FastApiBuilder


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup: Create database tables
    logger.info("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(bind=sync_conn))
    logger.info("Database tables created successfully")

    yield  # The application runs here

    # Shutdown: Add any cleanup code here if needed
    logger.info("Application shutting down...")


app = (
    FastApiBuilder(
        title="E-commerce project",
        version="0.0.1",
        logger=logger,
        env=app_settings.env,
        lifespan=lifespan,
    )
    .handle_exceptions()
    .add_cors_middleware(["*"])
    .add_health_endpoint()
    .add_root_router(root_router)
    .build()
)
