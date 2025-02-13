from fastapi import APIRouter

from api.dependencies import commander
from modules.commander import schemas as models
from modules.commander.service import AgentsCommander

router = APIRouter(
    tags=["portrainer commander api"],
    prefix="/commander",
)


@router.get("/get_environments", response_model=list[models.Environment])
def get_environments(service: AgentsCommander = commander) -> list[models.Environment]:
    return service.get_environments()


@router.get("/get_containers/{env_id}", response_model=list[models.Container])
def get_containers(env_id: int, service: AgentsCommander = commander) -> list[models.Container]:
    return service.get_containers(env_id=env_id)
