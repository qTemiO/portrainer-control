from typing import Annotated

from pydantic import Field
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, Form, HTTPException

import utils
from modules.commander import schemas as models
from modules.commander.service import AgentsCommander

router = APIRouter(
    tags=["portrainer commander api"],
    prefix="/commander",
)


@router.get("/environments")
def get_environments(service: AgentsCommander = Depends()) -> list[models.Environment]:
    return service.get_environments()


@router.get("/containers/{env_id}")
def get_containers(env_id: int, service: AgentsCommander = Depends()) -> list[models.Container]:
    return service.get_containers(env_id=env_id)


@router.post("/{environment_id}/{container_id}/restart")
def restart_container(
    environment_id: int, container_id: str, service: AgentsCommander = Depends()
) -> models.OperationsResponse:
    status_code, details = service.restart_container(env_id=environment_id, container_id=container_id)
    return utils.form_response(status_code=status_code, details=details)


@router.post("/{environment_id}/{container_id}/start")
def start_container(
    environment_id: int, container_id: str, service: AgentsCommander = Depends()
) -> models.OperationsResponse:
    status_code, details = service.start_container(env_id=environment_id, container_id=container_id)
    return utils.form_response(status_code=status_code, details=details)


@router.post("/{environment_id}/{container_id}/stop")
def stop_container(
    environment_id: int, container_id: str, service: AgentsCommander = Depends()
) -> models.OperationsResponse:
    status_code, details = service.stop_container(env_id=environment_id, container_id=container_id)
    return utils.form_response(status_code=status_code, details=details)


@router.get("/registries")
def get_registries(service: AgentsCommander = Depends()) -> list[models.Registry]:
    return service.get_registries()


@router.post("/image_to_registry")
async def image_to_registry(
    tasks: BackgroundTasks,
    name: str = "image-name",
    tag: str = "latest",
    registry_host: str = "localhost",
    registry_port: int = 5000,
    file: UploadFile = File(...),
    service: AgentsCommander = Depends(),
    ) -> models.OperationsResponse:
    """
    Upload a Docker image to a registry.

    This endpoint allows you to upload a Docker image to a specified registry.
    You need to provide the image details as a JSON string and the image file.
    """
    filename = await utils.save_file(file)
    status_code, details = service.load_image_from_tar_file_to_registry(name=name, tag=tag, uploaded_file_path=filename, registry_address=f"{registry_host}:{registry_port}")
    tasks.add_task(utils.delete_file, filename)
    return utils.form_response(status_code=status_code, details=details)
