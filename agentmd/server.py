"""Base provider class."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from agentmd.config import config_manager
from agentmd.models import AIModel, ChatMessage
from agentmd.utils import get_logger

logger = get_logger(__name__)


class BaseProvider(ABC):
    def __init__(self, provider_name: str):
        self.provider_name = provider_name
        self.config = config_manager.get_provider_config(provider_name)
        self.api_key = self.config.get("api_key") if self.config else None

    @abstractmethod
    async def sync_models(self) -> bool:
        pass

    @abstractmethod
    async def chat(self, message: str, model: str, messages: List[ChatMessage]) -> str:
        pass

    def get_models(self) -> List[AIModel]:
        if not self.config:
            return []
        return self.config.get("models", [])

    def save_models(self, models: List[Dict[str, Any]]) -> None:
        config_manager.update_provider_models(self.provider_name, models)
        logger.info(f"Saved {len(models)} models for {self.provider_name}")

    def get_api_key(self) -> Optional[str]:
        if not self.api_key:
            logger.warning(f"API key not found for {self.provider_name}")
        return self.api_key
