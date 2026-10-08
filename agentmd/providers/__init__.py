"""API routes module."""

from fastapi import APIRouter

from agentmd.api.auth import router as auth_router
from agentmd.api.chat_routes import router as chat_router
from agentmd.api.models_routes import router as models_router
from agentmd.api.rag_routes import router as rag_router
from agentmd.api.settings_routes import router as settings_router

router = APIRouter()

router.include_router(auth_router, tags=["auth"])
router.include_router(settings_router, tags=["settings"])
router.include_router(models_router, tags=["models"])
router.include_router(chat_router, tags=["chat"])
router.include_router(rag_router, tags=["rag"])
