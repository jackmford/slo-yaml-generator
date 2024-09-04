import pytest
from slo_yaml_generator.main import open_config_file

@pytest.fixture
def config():
    return {
      "resource_name": "This is a test project",
      "description": "This is a test description for Jack's little tool for SLO consulting"
    }

def test_open_config_file(config):
    json_obj = config

    r = open_config_file("./example-configs/project.json")

    assert r == json_obj

def test_bad_config_file():
    with pytest.raises(SystemExit):
        open_config_file("bad path")

