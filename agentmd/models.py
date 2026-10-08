"""Configuration management for AgentMd."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "agentmd"
    version: str = "0.1.0"
    description: str = "Custom CLI for prompt automation and context engineering"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 1010
    database_path: str = "rag.db"
    uploads_dir: str = "uploads"
    files_dir: str = "files"
    archive_dir: str = "archive"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()


class ConfigManager:
    def __init__(self, config_file: Optional[str] = None):
        if config_file is None:
            config_dir = Path.home() / ".agentmd"
            config_dir.mkdir(exist_ok=True)
            config_file = config_dir / "config.json"
        else:
            config_file = Path(config_file)
            config_file.parent.mkdir(parents=True, exist_ok=True)

        self.config_file = config_file
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "active_provider": "gemini",
            "model_selected": None,
            "last_updated": datetime.now().strftime("%Y%m%d"),
            "providers": {
                "gemini": None,
                "ollama": None,
                "openai": None,
                "claude": None,
                "deep-seek": None,
                "mistral": None,
            },
        }

    def _save_config(self) -> None:
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=2, default=str)

    def get(self, key: str, default: Any = None) -> Any:
        current = self._config
        for part in key.split("."):
            if not isinstance(current, dict) or part not in current:
                return default
            current = current[part]
        return current

    def set(self, key: str, value: Any) -> None:
        current = self._config
        keys = key.split(".")
        for part in keys[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        current[keys[-1]] = value
        self._save_config()

    def get_providers(self) -> list[str]:
        providers = self.get("providers")
        return list(providers.keys()) if providers else []

    def get_provider_config(self, provider: str) -> Optional[Dict[str, Any]]:
        return self.get(f"providers.{provider}")

    def set_provider_config(self, provider: str, config: Dict[str, Any]) -> None:
        self.set(f"providers.{provider}", config)

    def clear_provider_apikey(self, provider: str) -> None:
        provider_config = self.get_provider_config(provider) or {}
        provider_config["api_key"] = None
        self.set_provider_config(provider, provider_config)

    def get_model_selected(self) -> Optional[str]:
        return self.get("model_selected")

    def set_model_selected(self, model: str) -> None:
        self.set("model_selected", model)

    def update_provider_models(self, provider: str, models: list) -> None:
        provider_config = self.get_provider_config(provider) or {}
        provider_config["models"] = models
        self.set_provider_config(provider, provider_config)
        self.set("last_updated", datetime.now().strftime("%Y%m%d"))

    def to_dict(self) -> Dict[str, Any]:
        return self._config.copy()


config_manager = ConfigManager()
