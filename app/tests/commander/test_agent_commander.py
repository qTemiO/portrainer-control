from loguru import logger

from modules.commander.service import AgentsCommander


def test_agents_commander():
    commander = AgentsCommander()

    endpoints = commander.get_all_endpoints()

    assert endpoints != {}

    ids = [subresponse.get("Id") for subresponse in endpoints]
    names = [subresponse.get("Name") for subresponse in endpoints]

    assert ids != []
    assert names != []

    for id_ in ids:
        containers = commander.get_all_containers_by_env_id(id_)

        for container in containers:

            a = container
            x = a
