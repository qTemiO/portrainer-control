from typing import Optional
import requests
import json


class AgentsCommander():

    def __init__(self, host: str, port: int):
        self.agent_url = f"http://{host}:{port}/"
        self.access_token = ""

    def auth(
        self,
        login: str,
        password: str,
    ):
        response = requests.post(
            self.agent_url + "/api/auth", {
                "Username": login,
                "Password": password,
            }, timeout=60.0
        )
        return response

    def stop_container(self):
        pass

    def start_container(
        self,
        agent_url: str,
        container_name: str,
    ):
        pass
        # requests.post()

    def get_all_environments(
        self
    ):
        response = requests.get(
            url=self.agent_url + "/api/endpoint_groups", headers={"X-API-Key": self.access_token},
            data={"all": True}, timeout=60.0
        )    
        return response.text

    def get_all_endpoints(
        self,    
    ):
        response = requests.get(
            url=self.agent_url + f"/api/endpoints", headers={"X-API-Key": self.access_token},
            data={"all": True}, timeout=60.0
        )
        return json.loads(response.text)
            
    def get_all_containers_by_env_id(
        self,
        env_id: int,
    ):
        response = requests.get(
            url=self.agent_url + f"/api/endpoints/{env_id}/docker/containers/json", headers={"X-API-Key": self.access_token},
            data={"all": True}, timeout=60.0
        )
        return response.text
