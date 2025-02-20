import os
import json
from enum import Enum
from typing import Optional

import aiofiles
from loguru import logger
from fastapi import UploadFile

from modules.commander.schemas import OperationsResponse, ImageLoadingPayload


class ServiceStatuses(Enum):
    HTTP_OK = 200
    HTTP_INTERNAL_ERROR = 500
    HTTP_PORTAINER_UNAVAILIABLE = 503
    HTTP_UNPROCESSABLE_ENTITY = 422


status_details = {
    "200": "All good",
    "500": "Internal error occured",
    "503": "Portainer service is unavailiable or requests is forbidden",
    "422": "Wrong data sent",
}


async def save_file(file: UploadFile):
    filepath = f"../tmp/{file.filename}"

    async with aiofiles.open(filepath, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    return filepath


async def delete_file(filepath: str):
    os.unlink(filepath)


def form_response(status_code: int, details: Optional[str] = None) -> OperationsResponse:
    details = details if details else status_details.get(f"{status_code}")
    return OperationsResponse(status_code=status_code, details=details)


def from_form_to_pydantic(item: str):
    try:
        data = json.loads(item)
        return ImageLoadingPayload.model_validate(data)
    except Exception as error:
        logger.error(error)
        return None
