"""AgentMd package."""

__version__ = "0.1.0"
__author__ = "AntsugDev"

from agentmd.config import config_manager
from agentmd.database.database import db

__all__ = ["config_manager", "db"]
