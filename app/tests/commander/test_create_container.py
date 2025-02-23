from modules.commander import schemas as models
from modules.commander.service import AgentsCommander


def test_create_container():
    commander = AgentsCommander()

    item = models.ContainersCreatePayload(
        env_id=2,
        registry_host="localhost",
        registry_port="5000",
        image_name="example_to_registry",
        container_name="example_from_api",
        ports=["8010:8010", "8011:8011"],
        cmd=["python"],
    )
    result, _ = commander.create_container(item=item)

    assert result == 200 or result == 201
