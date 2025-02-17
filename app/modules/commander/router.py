from fastapi import APIRouter, Depends, Response, UploadFile, File

from utils import form_response
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
    return form_response(status_code=status_code, details=details)


@router.post("/{environment_id}/{container_id}/start")
def start_container(
    environment_id: int, container_id: str, service: AgentsCommander = Depends()
) -> models.OperationsResponse:
    status_code, details = service.start_container(env_id=environment_id, container_id=container_id)
    return form_response(status_code=status_code, details=details)


@router.post("/{environment_id}/{container_id}/stop")
def stop_container(
    environment_id: int, container_id: str, service: AgentsCommander = Depends()
) -> models.OperationsResponse:
    status_code, details = service.stop_container(env_id=environment_id, container_id=container_id)
    return form_response(status_code=status_code, details=details)


@router.get("/registries")
def get_registries(service: AgentsCommander = Depends()) -> list[models.Registry]:
    return service.get_registries()


# TODO: add pydantic schema + load logic + requests + asyncio?
# @router.post("/image/load")
# def load_image(file: UploadFile, service: AgentsCommander = Depends(), ):
#     status = service.load_image_from_tar_file(file, )
