from loguru import logger

from modules.commander.service import AgentsCommander

# agent_address = "https://192.168.0.35:19001/"
import requests

def test_agents_commander():
    commander = AgentsCommander(
        host="192.168.0.59",
        port=9000,
    )

    # response = commander.get_all_containers_by_env_id(4)
    # logger.debug(response)

    response = commander.get_all_endpoints()
    # logger.debug(response)
    logger.debug([subresponse.get("Id") for subresponse in response])
    logger.debug([subresponse.get("Name") for subresponse in response])
    logger.debug(response[0].keys())
    # logger.debug(len(response))
    # response = commander.get_all_environments()
    # logger.debug(response)

