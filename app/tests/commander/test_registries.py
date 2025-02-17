from modules.commander.service import AgentsCommander


def test_agents_commander_registries():
    commander = AgentsCommander()

    registries = commander.request_manager.get_registries()

    for registgry in registries:
        info = commander.request_manager.get_registry_info(registgry.get("Id"))

        assert info is not None
