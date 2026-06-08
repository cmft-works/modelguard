from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "ModelGuard AI"
    database_url: str = "sqlite:///./modelguard.db"
    monthly_budget_default: float = 10000.0
    environment: str = "dev"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    gemini_api_key: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
