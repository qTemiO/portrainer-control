from modules.commander.service import AgentsCommander


def test_agents_commander():
    commander = AgentsCommander()

    envs = commander.get_environments()

    env_id = envs[1].id
    containers = commander.get_containers(env_id)
    container_id = containers[4].id

    commander.stop_container(env_id=env_id, container_id=container_id)
    commander.start_container(env_id=env_id, container_id=container_id)
    commander.restart_container(env_id=env_id, container_id=container_id)
