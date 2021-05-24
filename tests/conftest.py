import json
import os
import pytest


@pytest.fixture
def lims_json_file():
    return os.path.join("resources", "snpseq_data_example.json")


@pytest.fixture
def lims_json_obj(lims_json_file):
    with open(lims_json_file) as fh:
        return json.load(fh)
