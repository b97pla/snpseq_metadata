from snpseq_metadata.models.sequencing_run import NGIUppsalaRun, SequencingRun


class TestSequencingRun:
    def test_to_json(self):
        run_alias = "this-is-a-run-alias"
        run_center = "this-is-a-run-center"
        run = SequencingRun(run_alias=run_alias, run_center=run_center)

        expected_json = {
            "@alias": run_alias,
            "@run_center": run_center,
            "EXPERIMENT_REF": {},
            "DATA_BLOCK": {"FILES": {"FILE": []}},
        }

        assert run.to_json() == expected_json


class TestNGIUppsalaRun:
    def test_to_json(self):
        run_alias = "this-is-a-run-alias"
        run_center = "National Genomics Infrastructure, Uppsala"
        run = NGIUppsalaRun(run_alias=run_alias)

        expected_json = {
            "@alias": run_alias,
            "@run_center": run_center,
            "EXPERIMENT_REF": {},
            "DATA_BLOCK": {"FILES": {"FILE": []}},
        }

        assert run.to_json() == expected_json
