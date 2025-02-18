from modules.commander.service import AgentsCommander


def test_push():

    commander = AgentsCommander()

    name_with_registry = "localhost:5000/example_to_registry:test"
    response = commander.request_manager.push_image(name=name_with_registry, tag="test")
    assert response