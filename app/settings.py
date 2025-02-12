import datetime

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(Path(__file__).parent.parent.joinpath(".env")))
    # Service configs
    ## Healthcheck
    IS_EXCEPTIONS_RAISED: bool = False
    EXCEPTION_DETAIL: str = "all good"
    DATE_FROM_LAST_EXCEPTION_CAUSED: Optional[datetime.datetime] = None

    HOST: Optional[str] = "0.0.0.0"
    PORT: Optional[int] = 8102
    NVIDIA_VISIBLE_DEVICE: int = 0
    # Optional services

    ## Translator
    TRANSLATOR_SERVICE_HOST: str
    TRANSLATOR_SERVICE_PORT: int
    TRANSLATOR_SERVICE_PROTOCOL: str

    ## LLaMa
    LLM_SERVICE_HOST: str
    LLM_SERVICE_PORT: int
    LLM_SERVICE_PROTOCOL: str

    ## Geocoder
    NOMINANTIM_SERVICE_PROTOCOL: str
    NOMINANTIM_SERVICE_HOST: str
    NOMINANTIM_SERVICE_PORT: int

    ## RabbitMQ
    RABBIT_USER: str
    RABBIT_PASSWORD: str
    RABBIT_HOST: str
    RABBIT_PORT: int
    RABBIT_QUEUE: str

    ## DB repository
    NEWS_DATABASE_SERVICE_PROTOCOL: str
    NEWS_DATABASE_SERVICE_HOST: str
    NEWS_DATABASE_SERVICE_PORT: int

    ## News weeder (embeddings hub)
    NEWS_WEEDER_PROTOCOL: str
    NEWS_WEEDER_HOST: str
    NEWS_WEEDER_PORT: int

    @property
    def NEWS_WEEDER_URL(cls):
        return f"{cls.NEWS_WEEDER_PROTOCOL}://{cls.NEWS_WEEDER_HOST}:{cls.NEWS_WEEDER_PORT}/weeder"

    @property
    def NEWS_DATABASE_URL(cls):
        return f"{cls.NEWS_DATABASE_SERVICE_PROTOCOL}://{cls.NEWS_DATABASE_SERVICE_HOST}:{cls.NEWS_DATABASE_SERVICE_PORT}"

    @property
    def NOMINANTIM_URL(cls):
        return f"{cls.NOMINANTIM_SERVICE_PROTOCOL}://{cls.NOMINANTIM_SERVICE_HOST}:{cls.NOMINANTIM_SERVICE_PORT}/search?q="

    @property
    def TRANSLATOR_URL(cls):
        return f"{cls.TRANSLATOR_SERVICE_PROTOCOL}://{cls.TRANSLATOR_SERVICE_HOST}:{cls.TRANSLATOR_SERVICE_PORT}/translator/text"

    @property
    def RABBIT_URL(cls):
        return f"amqp://{cls.RABBIT_USER}:{cls.RABBIT_PASSWORD}@{cls.RABBIT_HOST}:{cls.RABBIT_PORT}"

    @property
    def LLM_URL(cls):
        return f"{cls.LLM_SERVICE_PROTOCOL}://{cls.LLM_SERVICE_HOST}:{cls.LLM_SERVICE_PORT}/v1"


settings = Settings()
