from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:pass@localhost/ai_agents"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # AI APIs
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # Telegram
    telegram_bot_token: str = ""

    # App
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
