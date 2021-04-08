from snpseq_metadata.models.experiment import Experiment

from tests.models.test_flowcell import TestFlowcell


class TestExperiment:
    def test_to_json(self):
        field_dict = {
            "experiment_name": "this-is-an-experiment-name",
            "sample_project": "this-is-a-sample-project",
            "sample_id": "this-is-a-sample-id",
        }
        field_dict.update({k: str(v) for v, k in enumerate(["a", "b", "c"])})
        expected_json = {"@refname": field_dict["experiment_name"]}
        experiment_obj = Experiment(**field_dict)

        assert experiment_obj.to_json() == expected_json

    def test_from_samplesheet_row(self):
        samplesheet_data = TestFlowcell._return_samplesheet_data()
        for samplesheet_row in samplesheet_data:
            experiment = Experiment.from_samplesheet_row(samplesheet_row)
            assert (
                experiment.experiment_name
                == samplesheet_row["description"].split(":")[-1]
            )
            for key, value in samplesheet_row.items():
                assert getattr(experiment, key) == value
