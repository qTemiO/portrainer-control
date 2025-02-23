from pydantic import BaseModel, Field


class OperationsResponse(BaseModel):
    status_code: int = 500
    details: str = "Unknown exception occured"


class ImageLoadingPayload(BaseModel):
    name: str = Field(default="image-name")
    tag: str = Field(default="latest")
    registry_host: str = Field(default="localhost")
    registry_port: int = Field(default=5000)


class ContainersCreatePayload(BaseModel):
    env_id: int
    registry_host: str = "localhost"
    registry_port: int = 5000
    image_name: str = Field("image-from-registry")
    image_tag: str = "latest"
    container_name: str = Field("my-container")
    ports: list[str] = Field(["8100:8100", "8101:8101"])
    cmd: list[str] = Field(["this", "command", "is", "required"])
