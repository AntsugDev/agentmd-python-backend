"""FastAPI application factory."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from agentmd.api import router as api_router
from agentmd.config import settings
from agentmd.database import db
from agentmd.utils import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("AgentMd server starting up")
    yield
    logger.info("AgentMd server shutting down")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description=settings.description,
        version=settings.version,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["x-api-key", "Content-Disposition"],
    )

    app.include_router(api_router, prefix="/api")

    @app.get("/up")
    async def health_check():
        return {"status": "ok"}

    public_dir = Path(__file__).resolve().parent.parent / "public"
    if public_dir.exists():
        app.mount("/", StaticFiles(directory=str(public_dir), html=True), name="static")

    return app
