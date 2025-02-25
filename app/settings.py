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

    # Registry
    REGISTRY_PROTOCOL: str
    REGISTRY_HOST: str
    REGISTRY_PORT: int

    # Opensearch
    OPENSEARCH_DASHBOARDS_PROTOCOL: str
    OPENSEARCH_DASHBOARDS_HOST: str
    OPENSEARCH_DASHBOARDS_PORT: int

    OPENSEARCH_DASHBOARDS_RO_LOGIN: str
    OPENSEARCH_DASHBOARDS_RO_PASSWORD: str

    @property
    def portrainer_url(self):
        return f"{self.PORTRAINER_PROTOCOL}://{self.PORTRAINER_HOST}:{self.PORTRAINER_PORT}"

    @property
    def registry_url(self):
        return f"{self.REGISTRY_PROTOCOL}://{self.REGISTRY_HOST}:{self.REGISTRY_PORT}"

    @property
    def opensearch_url(self):
        return f"{self.OPENSEARCH_DASHBOARDS_PROTOCOL}://{self.OPENSEARCH_DASHBOARDS_HOST}:{self.OPENSEARCH_DASHBOARDS_PORT}"


settings = Settings()
