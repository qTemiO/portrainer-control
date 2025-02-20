from typing import Optional

from fastapi import HTTPException
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

    def _parse_ports(self, ports: list[dict]):
        total_ports = [f"{port.get('PrivatePort')}:{port.get('PublicPort')}" for port in ports]
        return list(set(total_ports))

    def get_images(self, registry_host: str, registry_port: int):
        registry_url = f"https://{registry_host}:{registry_port}"
        try:
            images = self.request_manager.get_all_images_registry(registry_url)
        except Exception as error:
            raise HTTPException(status_code=503, detail=f"Registry service unavailiable {error}")
        return [models.Image(name=image) for image in images.get("repositories")]

    def get_environments(self):
        endpoints = self.request_manager.get_all_endpoints()

        return [
            models.Environment(
                id=endpoint.get("Id"),
                name=endpoint.get("Name"),
                url=endpoint.get("URL"),
                status=endpoint.get("Status"),
                total_containers=endpoint.get("Snapshots")[0].get("ContainerCount"),
                running_containers=endpoint.get("Snapshots")[0].get("RunningContainerCount"),
                stopped_containers=endpoint.get("Snapshots")[0].get("StoppedContainerCount"),
                healthy_containers=endpoint.get("Snapshots")[0].get("HealthyContainerCount"),
                unhealthy_containers=endpoint.get("Snapshots")[0].get("UnhealthyContainerCount"),
                stack_count=endpoint.get("Snapshots")[0].get("StackCount"),
            ) for endpoint in endpoints
        ]

    def create_environment(self, name: str, url: str):
        try:
            response = self.request_manager.create_environment(name=name, url=url)
            if response.statis_code is 200:
                return ServiceStatuses.HTTP_OK.value, None
            else:
                return ServiceStatuses.HTTP_UNPROCESSABLE_ENTITY.value, "Name or URL is invalid"
        except Exception as error:
            logger.error(f"Error occured creating endpoint {error}")
            return ServiceStatuses.HTTP_PORTAINER_UNAVAILIABLE.value, f"Error occured creating endpoint {error}"

    def get_containers(self, env_id: int):
        containers = self.request_manager.get_all_containers_by_env_id(env_id=env_id)

        return [
            models.Container(
                id=container.get("Id"),
                names=container.get("Names"),
                image=container.get("Image"),
                state=container.get("State"),
                ports=self._parse_ports(container.get("Ports")),
            ) for container in containers
        ]

    def create_container(self, env_id: int, image_name: str, registry_host: str,
                         registry_port: int) -> tuple[int, Optional[str]]:
        try:
            registry_url = f"https://{registry_host}:{registry_port}/"
            response = self.request_manager.create_container(
                env_id=env_id, image_name=image_name, registry_url=registry_url
            )
            if response.status_code is 201:
                return ServiceStatuses.HTTP_OK.value, None
            else:
                return ServiceStatuses.HTTP_UNPROCESSABLE_ENTITY.value, "Error creating container"
        except Exception as error:
            logger.error(error)
            return ServiceStatuses.HTTP_PORTAINER_UNAVAILIABLE.value, str(error)

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

    def delete_container(self, env_id: int, container_id: str) -> tuple[int, Optional[str]]:
        try:
            response = self.request_manager.delete_container(env_id=env_id, container_id=container_id)
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

    def load_image_from_tar_file_to_registry(
        self,
        name: str,
        tag: str,
        uploaded_file_path: str,
        registry_address: str,
        main_env_id: int = 2,
    ):
        # Step 1st load to server
        response = self.request_manager.load_image_to_main_server(
            uploaded_file_path=uploaded_file_path, name=name, tag=tag, main_env_id=main_env_id
        )

        if response.status_code != 200:
            error = "Error creating image from file"
            logger.error(error)
            return ServiceStatuses.HTTP_PORTAINER_UNAVAILIABLE, error

        # Step 2nd tag like registry
        response = self.request_manager.tag_image(
            new_name=name, name=name, registry_address=registry_address, new_tag=tag, tag=tag
        )

        if response.status_code != 201:
            error = "Error tagging image"
            logger.error(error)
            return ServiceStatuses.HTTP_PORTAINER_UNAVAILIABLE, error

        # Step 3rd push to registry
        response = self.request_manager.push_image(name=name, tag=tag, repository=registry_address)

        if response.status_code != 200:
            error = "Error pushing image"
            logger.error(error)
            return ServiceStatuses.HTTP_PORTAINER_UNAVAILIABLE, error

        return ServiceStatuses.HTTP_OK, "success"
