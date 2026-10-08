"""Authentication and session routes."""

from fastapi import APIRouter

from agentmd.models import SessionResponse
from agentmd.utils import SessionManager, get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/session", response_model=SessionResponse)
async def get_session():
    api_key = SessionManager.generate_session_key()
    logger.info("New session generated")
    return SessionResponse(api_key=api_key)
