import os
import pytest
import json

from snpseq_metadata.models.ngi_models import (
    NGIStudyRef,
    NGISampleDescriptor,
    NGILibrary,
    NGIExperiment,
    NGISequencingPlatform,
    NGIExperimentSet,
)


@pytest.fixture
def _prefix():
    return "this-is-a-"


@pytest.fixture
def model_fields(_prefix):
    return {
        "project_id": f"{_prefix}project",
        "sample_id": f"{_prefix}sample",
        "description": f"{_prefix}description",
        "application": f"{_prefix}application",
        "sample_type": f"{_prefix}sample_type",
        "library_kit": f"{_prefix}library_kit",
        "experiment_alias": f"{_prefix}experiment_alias",
        "experiment_title": f"{_prefix}experiment_title",
        "is_paired": True,
        "model_name": "novaseq",
    }


@pytest.fixture
def temp_output(tmpdir):
    return os.path.join(tmpdir, "ngi_experiment_model.json")


class TestNGIModel:
    def test_model(self, model_fields, temp_output):
        project = NGIStudyRef(project_id=model_fields["project_id"])
        sample = NGISampleDescriptor(
            sample_id=f"{project.project_id}_{model_fields['sample_id']}"
        )
        library = NGILibrary(
            sample=sample,
            description=model_fields["description"],
            application=model_fields["application"],
            sample_type=model_fields["sample_type"],
            library_kit=model_fields["library_kit"],
            is_paired=model_fields["is_paired"],
        )
        platform = NGISequencingPlatform(model_name=model_fields["model_name"])
        experiment = NGIExperiment(
            alias=model_fields["experiment_alias"],
            title=model_fields["experiment_title"],
            project=project,
            library=library,
            platform=platform,
        )
        experiment_set = NGIExperimentSet(experiments=[experiment])

        with open(temp_output, "w") as fh:
            json.dump(experiment_set.to_json(), fh, indent=2)

        with open(temp_output) as fh:
            json_obj = json.load(fh)

        parsed_experiment_set = NGIExperimentSet.from_json(json_obj)

        assert parsed_experiment_set == experiment_set
