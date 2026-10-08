"""RAG (Retrieval Augmented Generation) routes."""

from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, Form, UploadFile

from agentmd.api.dependencies import verify_config, verify_session
from agentmd.config import settings
from agentmd.database import db
from agentmd.utils import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/rag/files")
async def upload_rag_files(
    files: List[UploadFile] = File(...),
    argument: str = Form(...),
    _: None = Depends(verify_session),
    __: None = Depends(verify_config),
):
    uploads_dir = Path(settings.uploads_dir)
    uploads_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []
    for file in files:
        if not file.filename:
            continue

        file_path = uploads_dir / file.filename
        content = await file.read()
        with open(file_path, "wb") as handle:
            handle.write(content)

        ext = file.filename.split(".")[-1] if "." in file.filename else ""
        db.execute(
            """
            INSERT INTO FILES (FILE_NAME, CONTENT, TAG, STATUS_ID, MODEL_USED, MIME_TYPE, EXT)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (file.filename, None, argument, 1, None, file.content_type or "application/octet-stream", ext),
        )
        db.commit()
        saved_files.append(file.filename)

    return {
        "status": "success",
        "uploaded_files": saved_files,
        "message": f"Uploaded {len(saved_files)} files for RAG processing",
    }


@router.get("/rag/files")
async def list_rag_files(
    _: None = Depends(verify_session),
    __: None = Depends(verify_config),
):
    cursor = db.execute("SELECT * FROM FILES")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


@router.get("/rag/tags")
async def get_tags(
    _: None = Depends(verify_session),
    __: None = Depends(verify_config),
):
    cursor = db.execute("SELECT DISTINCT TAG FROM FILES WHERE TAG IS NOT NULL")
    tags = [row[0] for row in cursor.fetchall()]
    return {"tags": tags}
