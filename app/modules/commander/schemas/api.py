from pydantic import BaseModel, Field


class OperationsResponse(BaseModel):
    status_code: int = 500
    details: str = "Unknown exception occured"


class ImageLoadingPayload(BaseModel):
    name: str = Field(default="image-name")
    tag: str = Field(default="latest")
    registry_host: str = Field(default="localhost")
    registry_port: int = Field(default=5000)
