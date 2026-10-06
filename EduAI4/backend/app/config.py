"""All settings come from environment variables / .env (no hard-coded secrets)."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Hosts often give "postgres://..."; SQLAlchemy needs "postgresql://..."
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./eduai.db").replace("postgres://", "postgresql://", 1)
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    TOKEN_MINUTES = int(os.getenv("TOKEN_MINUTES", "10080"))
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    AI_MODEL = os.getenv("AI_MODEL", "claude-sonnet-5-5")
    AI_RATE_LIMIT = int(os.getenv("AI_RATE_LIMIT_PER_HOUR", "20"))
    WEAK_THRESHOLD = int(os.getenv("WEAK_THRESHOLD", "60"))  # accuracy % below this = weak


settings = Settings()
