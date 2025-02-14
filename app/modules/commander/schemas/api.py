from pydantic import BaseModel


class OperationsResponse(BaseModel):
    status_code: int = 500
    details: str = "Unknown exception occured"
