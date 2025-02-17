from typing import Optional

from loguru import logger

from utils import ServiceStatuses
from settings import settings
from modules.commander import schemas as models
from modules.commander.core import CoreRequests


class AgentsCommander():

    def __init__(self):
        # Core manager of portrainer\dockerAPI server
        self.request_manager = CoreRequests(
            portrainer_url=settings.portrainer_url,
            access_token=settings.PORTAINER_ACCESS_KEY,
        )

    def get_environments(self):
        endpoints = self.request_manager.get_all_endpoints()

        return [models.Environment(id=endpoint.get("Id"), name=endpoint.get("Name")) for endpoint in endpoints]

    def get_containers(self, env_id: int):
        containers = self.request_manager.get_all_containers_by_env_id(env_id=env_id)

        return [
            models.Container(
                id=container.get("Id"), names=container.get("Names"), image=container.get("Image"),
                state=container.get("State")
            ) for container in containers
        ]

    def stop_container(self, env_id: int, container_id: str) -> tuple[int, Optional[str]]:
        try:
            response = self.request_manager.stop_container(env_id=env_id, container_id=container_id)
            if response.status_code is 204:
                return ServiceStatuses.HTTP_OK.value, None
            else:
                return ServiceStatuses.HTTP_UNPROCESSABLE_ENTITY.value, "Stopping container not found"
        except Exception as error:
            logger.error(error)
            return ServiceStatuses.HTTP_PORTAINER_UNAVAILIABLE.value, str(error)

    def start_container(self, env_id: int, container_id: str) -> tuple[int, Optional[str]]:
        try:
            response = self.request_manager.start_container(env_id=env_id, container_id=container_id)
            if response.status_code is 204:
                return ServiceStatuses.HTTP_OK.value, None
            else:
                return ServiceStatuses.HTTP_UNPROCESSABLE_ENTITY.value, "Starting container not found"
        except Exception as error:
            logger.error(error)
            return ServiceStatuses.HTTP_PORTAINER_UNAVAILIABLE.value, str(error)

    def restart_container(self, env_id: int, container_id: str) -> tuple[int, Optional[str]]:
        try:
            response = self.request_manager.restart_container(env_id=env_id, container_id=container_id)
            if response.status_code is 204:
                return ServiceStatuses.HTTP_OK.value, None
            else:
                return ServiceStatuses.HTTP_UNPROCESSABLE_ENTITY.value, "Restarting container not found"
        except Exception as error:
            logger.error(error)
            return ServiceStatuses.HTTP_PORTAINER_UNAVAILIABLE.value, str(error)

    def get_registries(self):
        registries = self.request_manager.get_registries()

        return [models.Registry(id=registry.get("Id"), name=registry.get("Name")) for registry in registries]

    def load_image_from_tar_file(
        self,
        name: str,
        tag: str,
        uploaded_file_path: str,
        main_env_id: int,
    ):
        response = self.request_manager.load_image_to_main_server(
            uploaded_file_path=uploaded_file_path, name=name, tag=tag, main_env_id=main_env_id
        )

        if response.status_code == 200:
            return ServiceStatuses.HTTP_OK
        else:
            return ServiceStatuses.HTTP_PORTAINER_UNAVAILIABLE
