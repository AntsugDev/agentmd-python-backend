"""FastAPI dependencies for route authorization and verification."""

from typing import Optional

from fastapi import Header, HTTPException

from agentmd.config import config_manager
from agentmd.utils import SessionManager, get_logger

logger = get_logger(__name__)


async def verify_session(x_api_key: Optional[str] = Header(None, alias="x-api-key")) -> None:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Session not found")

    if not SessionManager.validate_session_key(x_api_key):
        raise HTTPException(status_code=401, detail="Session expired")


async def verify_config() -> None:
    config = config_manager.to_dict()
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
