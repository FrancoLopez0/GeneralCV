from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=['.env', '.env.example'],
        env_file_encoding='utf-8',
        case_sensitive=True,
    )

    HANDS_MODEL_MIN_CONFIDENCE: float
    HANDS_MODEL_MAX_NUM_HANDS: int = 4


settings = Settings()