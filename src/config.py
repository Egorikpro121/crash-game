"""Load config from settings.yaml and .env."""
from pathlib import Path
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = Path(os.getenv("DATA_DIR", str(PROJECT_ROOT / "data")))
DB_PATH = Path(os.getenv("DB_PATH", str(DATA_DIR / "tokens.db")))


def load_settings():
    path = CONFIG_DIR / "settings.yaml"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_moralis_api_key():
    return os.getenv("MORALIS_API_KEY", "").strip()


def get_telegram_config():
    return {
        "bot_token": os.getenv("TELEGRAM_BOT_TOKEN", "").strip(),
        "chat_id": os.getenv("TELEGRAM_CHAT_ID", "").strip(),
    }


def get_label_horizon_minutes() -> int:
    """Label horizon in minutes. Use TEST_LABEL_HORIZON_MINUTES for testing (e.g. 1)."""
    settings = load_settings()
    default = settings.get("labeling", {}).get("horizon_minutes", 30)
    env_val = os.getenv("TEST_LABEL_HORIZON_MINUTES", "").strip()
    if env_val.isdigit():
        return int(env_val)
    return default


def get_database_url() -> str:
    """Get database URL from environment."""
    return os.getenv(
        "DATABASE_URL",
        f"sqlite:///{DATA_DIR / 'crash_game.db'}"
    )


def get_redis_url() -> str:
    """Get Redis URL from environment."""
    return os.getenv("REDIS_URL", "redis://localhost:6379/0")


def get_secret_key() -> str:
    """Get secret key for JWT and encryption."""
    key = os.getenv("SECRET_KEY", "")
    if not key:
        raise ValueError("SECRET_KEY environment variable must be set")
    return key


def get_ton_api_key() -> str:
    """Get TON API key."""
    return os.getenv("TON_API_KEY", "").strip()


def get_ton_wallet_mnemonic() -> str:
    """Get TON wallet mnemonic."""
    return os.getenv("TON_WALLET_MNEMONIC", "").strip()
