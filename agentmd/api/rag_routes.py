"""Chat endpoint routes."""

from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from agentmd.api.dependencies import verify_config, verify_session
from agentmd.config import config_manager
from agentmd.utils import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/chat/{status}")
async def chat(
    status: str,
    message: str = Form(...),
    uuid_param: Optional[str] = Form(None, alias="uuid"),
    time: Optional[str] = Form(None),
    files: List[UploadFile] = File(default=[]),
    _: None = Depends(verify_session),
    __: None = Depends(verify_config),
):
    if status not in ["init", "next"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    selected_model = config_manager.get_model_selected()
    if not selected_model:
        raise HTTPException(status_code=400, detail="No model selected")

    chat_uuid = uuid_param or str(uuid4())[:10]
    logger.info(f"Chat {status} - UUID: {chat_uuid}, model: {selected_model}")

    return {
        "status": "success",
        "uuid": chat_uuid,
        "message": f"Chat {status} not yet implemented in Python backend",
    }


@router.post("/chat/compare/{status}")
async def chat_compare(
    status: str,
    message: str = Form(...),
    models: Optional[str] = Form(None),
    _: None = Depends(verify_session),
    __: None = Depends(verify_config),
):
    if status not in ["init", "next"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    logger.info(f"Chat compare {status} with models: {models}")

    return {
        "status": "success",
        "message": f"Chat compare {status} not yet implemented in Python backend",
    }
