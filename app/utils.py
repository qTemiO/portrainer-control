from typing import Optional
from enum import Enum

from loguru import logger
from modules.commander.schemas import OperationsResponse


class ServiceStatuses(Enum):
    HTTP_OK=200
    HTTP_INTERNAL_ERROR=500
    HTTP_PORTAINER_UNAVAILIABLE=503
    HTTP_UNPROCESSABLE_ENTITY=422

status_details = {
    "200": "All good",
    "500": "Internal error occured",
    "503": "Portainer service is unavailiable or requests is forbidden",
    "422": "Wrong data sent",   
}

def form_response(status_code: int, details: Optional[str] = None) -> OperationsResponse:
    details = details if details else status_details.get(f"{status_code}")
    return OperationsResponse(status_code=status_code, details=details)
