import json
import base64
from typing import Optional


import requests


class CoreRequests():

    def __init__(
        self,
        portrainer_url: str,
        access_token: str,
    ):
        self.portrainer_url = portrainer_url
        self.access_token = access_token

    def get_all_endpoints(
        self,
    ):
        response = requests.get(
            url=self.portrainer_url + "/api/endpoints",
            headers={"X-API-Key": self.access_token},
            data={"all": True},
            timeout=60.0,
            verify=False,
        )
        return json.loads(response.text)

    def get_all_containers_by_env_id(
        self,
        env_id: int,
    ):
        response = requests.get(
            url=self.portrainer_url + f"/api/endpoints/{env_id}/docker/containers/json?all=true",
            headers={"X-API-Key": self.access_token},
            timeout=60.0,
            verify=False,
        )
        return json.loads(response.text)

    def stop_container(self, env_id: int, container_id: str):
        response = requests.post(
            url=self.portrainer_url + f"/api/endpoints/{env_id}/docker/containers/{container_id}/stop",
            headers={"X-API-Key": self.access_token},
            timeout=60.0,
            verify=False,
        )
        return response

    def start_container(self, env_id: int, container_id: str):
        response = requests.post(
            url=self.portrainer_url + f"/api/endpoints/{env_id}/docker/containers/{container_id}/start",
            headers={"X-API-Key": self.access_token},
            timeout=60.0,
            verify=False,
        )
        return response

    def restart_container(self, env_id: int, container_id: str):
        response = requests.post(
            url=self.portrainer_url + f"/api/endpoints/{env_id}/docker/containers/{container_id}/restart",
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
        Loading image to main (command) environment

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
        registry_adress: Optional[str] = None,
        new_tag: Optional[str] = None,
        tag: Optional[str] = None,
        main_env_id: int = 2,
    ):
        """
        request to Docker Engine API to realise that command 

        <b> docker tag name:tag registry_adress/new_name:new_tag </b>
        """
        image_full_name = f"{name}:{tag}" if tag else f"{name}:latest"

        repo = f"{registry_adress}/{new_name}" if registry_adress else f"{new_name}"
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
        main_env_id: int = 2,
    ):
        if "/" not in name:
            return None
        payload = {}

        if tag:
            payload["tag"] = tag

        # Handling due to open registry without credentials
        auth_data = {
            "username": "",
            "password": "",
            "email": "",
            "serveraddress": "https://localhost:5000"
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
