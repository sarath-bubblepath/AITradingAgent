from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class SettingsError(ValueError):
    """Raised when required configuration is missing."""


@lru_cache
def get_reports_dir() -> Path:
    path = Path(os.getenv("REPORTS_DIR", "reports"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_alpaca_credentials() -> tuple[str, str]:
    key = os.getenv("ALPACA_API_KEY", "").strip()
    secret = os.getenv("ALPACA_SECRET_KEY", "").strip()
    if not key or not secret:
        raise SettingsError(
            "Missing ALPACA_API_KEY or ALPACA_SECRET_KEY. Add them to .env; "
            "market-data credentials are sufficient for this read-only MVP."
        )
    return key, secret


def get_alpaca_feed() -> str:
    return os.getenv("ALPACA_DATA_FEED", "iex").strip().lower()


def get_ollama_api_key() -> str:
    key = os.getenv("OLLAMA_API_KEY", "").strip()
    if not key:
        raise SettingsError(
            "Missing OLLAMA_API_KEY. Add it to .env to use Ollama cloud models."
        )
    return key
