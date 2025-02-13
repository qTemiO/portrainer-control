from typing import Annotated

from settings import settings

from modules.commander import schemas as models
from modules.commander.core import CoreRequests


class AgentsCommander():

    def __init__(
        self,
        portrainer_url: str = settings.portrainer_url,
        access_token: str = settings.PORTAINER_ACCESS_KEY,
    ):
        # Core manager of portrainer\dockerAPI server
        self.request_manager = CoreRequests(
            portrainer_url=portrainer_url,
            access_token=access_token,
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
