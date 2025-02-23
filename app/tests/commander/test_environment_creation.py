from modules.commander.service import AgentsCommander


def test_environment_creation():
    commander = AgentsCommander()

    url = "10.0.0.73:9001"
    name = "scanhost"
    commander.create_environment(name=name, url=url)
