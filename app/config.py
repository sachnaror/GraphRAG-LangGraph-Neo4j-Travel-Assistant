import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT_DIR / ".env"


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    openai_model: str
    app_secret_key: str | None
    neo4j_uri: str | None
    neo4j_username: str | None
    neo4j_password: str | None


@lru_cache
def get_settings() -> Settings:
    load_dotenv(dotenv_path=ENV_FILE)

    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        app_secret_key=os.getenv("APP_SECRET_KEY"),
        neo4j_uri=os.getenv("NEO4J_URI"),
        neo4j_username=os.getenv("NEO4J_USERNAME"),
        neo4j_password=os.getenv("NEO4J_PASSWORD"),
    )
