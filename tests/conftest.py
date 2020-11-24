import os
import pytest
import json
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

@pytest.fixture(scope="session")
def test_resources_dir():
    return os.path.join(os.path.dirname(__file__), 'resources')

@pytest.fixture
def rspec_metadata(test_resources_dir):
    rspec_path = os.path.join(test_resources_dir, "rspec.json")
    with open(rspec_path) as rspec_file:
        return json.load(rspec_file)