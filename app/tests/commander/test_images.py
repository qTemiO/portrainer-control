from modules.commander.service import AgentsCommander
from settings import settings


def test_images():
    commander = AgentsCommander()

    images = commander.get_images(settings.REGISTRY_HOST, settings.REGISTRY_PORT)
    assert images
