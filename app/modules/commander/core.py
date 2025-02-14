import json

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
            url=self.portrainer_url + f"/api/endpoints/{env_id}/docker/containers/json",
            headers={"X-API-Key": self.access_token},
            data={"all": True},
            timeout=60.0,
            verify=False,
        )
        return json.loads(response.text)

    def stop_container(
            self,
            env_id: int,
            container_id: str
        ):
        response = requests.post(
            url=self.portrainer_url + f"/api/endpoints/{env_id}/docker/containers/{container_id}/stop",
            headers={"X-API-Key": self.access_token},
            timeout=60.0,
            verify=False,
        )
        return response
        
    def start_container(
            self,
            env_id: int,
            container_id: str
        ):
        response = requests.post(
            url=self.portrainer_url + f"/api/endpoints/{env_id}/docker/containers/{container_id}/start",
            headers={"X-API-Key": self.access_token},
            timeout=60.0,
            verify=False,
        )
        return response
        
    def restart_container(
            self,
            env_id: int,
            container_id: str
        ):
        response = requests.post(
            url=self.portrainer_url + f"/api/endpoints/{env_id}/docker/containers/{container_id}/restart",
            headers={"X-API-Key": self.access_token},
            timeout=60.0,
            verify=False,
        )
        return response
        
