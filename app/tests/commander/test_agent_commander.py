from loguru import logger

from modules.commander.service import AgentsCommander


def test_agents_commander():
    commander = AgentsCommander()

    endpoints = commander.get_environments()

    assert endpoints is not {}

    ids = [environment.id for environment in endpoints]
    names = [environment.name for environment in endpoints]

    assert ids is not []
    assert names is not []

    for id_ in ids:
        containers = commander.get_containers(id_)

        assert containers is not []