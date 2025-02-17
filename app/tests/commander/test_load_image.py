from modules.commander.service import AgentsCommander


def test_load_image():
    commander = AgentsCommander()

    name = "example"
    tag = "latest"
    file_example = "tmp/example.tar.gz"

    commander.request_manager.load_image_to_main_server(uploaded_file_path=file_example, name=name, tag=tag)
