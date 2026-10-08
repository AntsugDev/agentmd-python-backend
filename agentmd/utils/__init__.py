from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AIModel(BaseModel):
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    input_token_limit: Optional[int] = None
    output_token_limit: Optional[int] = None
    version: Optional[str] = None


class ChatMessage(BaseModel):
    role: str
    text: str
    timestamp: Optional[datetime] = None


class SessionResponse(BaseModel):
    api_key: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None


class ProviderConfig(BaseModel):
    api_key: Optional[str] = None
    models: List[Dict[str, Any]] = Field(default_factory=list)
    base_url: Optional[str] = None


class AgentConfig(BaseModel):
    active_provider: str = "gemini"
    model_selected: Optional[str] = None
    last_updated: Optional[str] = None
    providers: Dict[str, Optional[Dict[str, Any]]] = Field(default_factory=lambda: {
        "gemini": None,
        "ollama": None,
        "openai": None,
        "claude": None,
        "deep-seek": None,
        "mistral": None,
    })
