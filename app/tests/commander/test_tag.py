from modules.commander.service import AgentsCommander


def test_tag():
    commander = AgentsCommander()

    image_name = "example"
    image_tag = "latest"

    new_image_name = "example_updated"
    new_image_tag = "0.0.1"

    commander.request_manager.tag_image(new_name=new_image_name, new_tag=new_image_tag, tag=image_tag, name=image_name)

    new_registry_name = "localhost:5000"
    new_image_name = "example_to_registry"
    new_image_tag = "test"

    commander.request_manager.tag_image(new_name=new_image_name, name=image_name, registry_adress=new_registry_name, new_tag=new_image_tag, tag=image_tag)
