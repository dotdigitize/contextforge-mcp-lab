"""Configuration helpers for ContextForge MCP Lab."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE_PATH = PROJECT_ROOT / "data" / "contextforge.db"


def _load_dotenv() -> None:
    """Load a small .env file without requiring runtime dependencies."""
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the local demo server."""

    database_path: Path


def get_settings() -> Settings:
    """Return settings loaded from environment variables."""
    _load_dotenv()
    database_path = Path(os.getenv("CONTEXTFORGE_DB_PATH", str(DEFAULT_DATABASE_PATH)))
    if not database_path.is_absolute():
        database_path = PROJECT_ROOT / database_path
    return Settings(database_path=database_path)

