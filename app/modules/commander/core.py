import json
import base64
import ast
from typing import Optional

from loguru import logger
import requests


class CoreRequests():

    def __init__(
        self,
        portrainer_url: str,
        access_token: str,
    ):
        self.portrainer_url = portrainer_url
        self.access_token = access_token

    def get_all_images_registry(self, registry_url: Optional[str] = None) -> dict:
        response = requests.get(
            url=registry_url + "/v2/_catalog",
            verify=False,
            timeout=60.0,
        )
        return json.loads(response.text)

    def get_all_endpoints(
        self,
    ) -> dict:
        response = requests.get(
            url=self.portrainer_url + "/api/endpoints",
            headers={"X-API-Key": self.access_token},
            data={"all": True},
            timeout=60.0,
            verify=False,
        )
        return json.loads(response.text)

    def create_environment(self, name: str, url: str) -> requests.Response:
        response = requests.post(
            url=self.portrainer_url + "/api/endpoints",
            headers={"X-API-Key": self.access_token},
            files={
                "Name": name,
                "EndpointCreationType": 1,
                "URL": url
            },
            timeout=60.0,
            verify=False,
        )
        return response

    def get_all_containers_by_env_id(
        self,
        env_id: int,
    ) -> dict:
        response = requests.get(
            url=self.portrainer_url + f"/api/endpoints/{env_id}/docker/containers/json?all=true",
            headers={"X-API-Key": self.access_token},
            timeout=60.0,
            verify=False,
        )
        if response.text == "":
            return []

        try:
            data = json.loads(response.text)
        except Exception as error:
            data = ast.literal_eval(response.text)
            logger.error(f"Json error {error}")
        return data

    def create_container(self, env_id: int, image_name: str, registry_url: str) -> requests.Response:
        payload = {
            "Image": f"{registry_url}/{image_name}",
        }

        response = requests.post(
            url=self.portrainer_url + f"/api/endpoints/{env_id}/docker/containers/create",
            headers={"X-API-Key": self.access_token},
            timeout=60.0,
            verify=False,
        )
        return response

    def stop_container(self, env_id: int, container_id: str) -> requests.Response:
        response = requests.post(
            url=self.portrainer_url + f"/api/endpoints/{env_id}/docker/containers/{container_id}/stop",
            headers={"X-API-Key": self.access_token},
            timeout=60.0,
            verify=False,
        )
        return response

    def start_container(self, env_id: int, container_id: str) -> requests.Response:
        response = requests.post(
            url=self.portrainer_url + f"/api/endpoints/{env_id}/docker/containers/{container_id}/start",
            headers={"X-API-Key": self.access_token},
            timeout=60.0,
            verify=False,
        )
        return response

    def restart_container(self, env_id: int, container_id: str) -> requests.Response:
        response = requests.post(
            url=self.portrainer_url + f"/api/endpoints/{env_id}/docker/containers/{container_id}/restart",
            headers={"X-API-Key": self.access_token},
            timeout=60.0,
            verify=False,
        )
        return response

    def delete_container(self, env_id: int, container_id: str) -> requests.Response:
        response = requests.delete(
            url=self.portrainer_url + f"/api/endpoints/{env_id}/docker/containers/{container_id}",
            headers={"X-API-Key": self.access_token},
            timeout=60.0,
            verify=False,
        )
        return response

    def get_registries(
        self,
    ):
        response = requests.get(
            url=self.portrainer_url + "/api/registries",
            headers={"X-API-Key": self.access_token},
            timeout=60.0,
            verify=False,
        )
        return json.loads(response.text)

    def get_registry_info(self, registry_id: int):
        response = requests.get(
            url=self.portrainer_url + f"/api/registries/{registry_id}",
            headers={"X-API-Key": self.access_token},
            timeout=60.0,
            verify=False,
        )
        return json.loads(response.text)

    def load_image_to_main_server(
        self,
        uploaded_file_path: str,
        name: str,
        tag: str,
        main_env_id: int = 2,
    ):
        """
        Loading image to main (local) environment
        First step of loading in registry
        Args:
            name: Name of loading image,
            tag: A tag of loading image,
            main_env_id: as usual it is 2, bcs of portainer default assets,
            uploaded_file_path: Path where image.tar.gz is
        """
        with open(uploaded_file_path, "rb") as image_file:
            response = requests.post(
                url=self.portrainer_url +
                f"/api/endpoints/{main_env_id}/docker/images/create?fromSrc=-&repo={name}&tag={tag}",
                verify=False,
                data=image_file,
                headers={
                    "X-API-Key": self.access_token,
                    "Content-Type": "application/x-tar"
                },
                timeout=60.0,
            )
        return response

    def tag_image(
        self,
        new_name: str,
        name: str,
        registry_address: Optional[str] = None,
        new_tag: Optional[str] = None,
        tag: Optional[str] = None,
        main_env_id: int = 2,
    ) -> requests.Response:
        """
        request to Docker Engine API to realise that command 

        <b> docker tag name:tag registry_adress/new_name:new_tag </b>
        """
        image_full_name = f"{name}:{tag}" if tag else f"{name}:latest"

        repo = f"{registry_address}/{new_name}" if registry_address else f"{new_name}"
        payload = {
            "repo": repo,
        }
        if new_tag:
            payload["tag"] = new_tag

        response = requests.post(
            url=self.portrainer_url + f"/api/endpoints/{main_env_id}/docker/images/{image_full_name}/tag",
            verify=False,
            params=payload,
            headers={
                "X-API-Key": self.access_token,
            },
            timeout=60.0,
        )
        return response

    def push_image(
        self,
        name: str,
        tag: Optional[str],
        repository: str,
        main_env_id: int = 2,
    ) -> requests.Request:
        """
        Push image with given host/image:tag to provided repository
        """
        if "/" not in name:
            name = repository + "/" + name
        payload = {}

        if tag:
            payload["tag"] = tag

        # Handling due to open registry without credentials
        auth_data = {
            "username": "",
            "password": "",
            "email": "",
            "serveraddress": "https://" + repository,
        }
        auth_json = json.dumps(auth_data).encode("utf-8")
        auth_header = base64.urlsafe_b64encode(auth_json).decode("utf-8")

        response = requests.post(
            url=self.portrainer_url + f"/api/endpoints/{main_env_id}/docker/images/{name}/push",
            verify=False,
            params=payload,
            headers={
                "X-API-Key": self.access_token,
                "X-Registry-Auth": auth_header
            },
            timeout=60.0,
        )

        return response
