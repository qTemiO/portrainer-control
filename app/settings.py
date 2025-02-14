from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(Path(__file__).parent.parent.joinpath(".env.production")))

    # Service
    HOST: Optional[str] = "0.0.0.0"
    PORT: Optional[int] = 8101

    # Portainer base
    PORTAINER_ACCESS_KEY: str
    PORTRAINER_PROTOCOL: str
    PORTRAINER_HOST: str
    PORTRAINER_PORT: int

    @property
    def portrainer_url(self):
        return f"{self.PORTRAINER_PROTOCOL}://{self.PORTRAINER_HOST}:{self.PORTRAINER_PORT}"


settings = Settings()
