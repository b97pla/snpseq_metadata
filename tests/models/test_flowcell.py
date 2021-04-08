import os

from snpseq_metadata.models.flowcell import Flowcell
import snpseq_metadata.utilities


class TestFlowcell:
    @staticmethod
    def _return_samplesheet(*args):
        return ["this-is-a-samplesheet"]

    @staticmethod
    def _return_alt_samplesheet(*args):
        return ["this-is-another-samplesheet"]

    @staticmethod
    def _return_samplesheet_data(*args):
        required_fields = ["sample_project", "sample_id"]
        additional_fields = [f"field_{i}" for i in range(3)]
        samplesheet_data = []
        for i in range(5):
            for j in range(2):
                samplesheet_data.append(
                    dict(zip(required_fields, [f"project_{i}{j}", f"sample_{i}{j}"]))
                )
                samplesheet_data[-1]["description"] = f"some-data:experiment-name-{i}"
                samplesheet_data[-1].update(
                    {k: f"{k}_{i}{j}" for k in additional_fields}
                )
        return samplesheet_data

    def test___init__(self):
        runfolder_name = "this-is-a-runfolder-name"
        runfolder_path = os.path.join(
            "/this", "is", "a", "runfolder", "path", runfolder_name
        )
        samplesheet_name = "this-is-a-supplied-samplesheet"
        fc = Flowcell(runfolder_path=runfolder_path, samplesheet=samplesheet_name)
        assert fc.runfolder_name == runfolder_name
        assert fc.samplesheet == samplesheet_name

    def test_samplesheet(self, monkeypatch):

        monkeypatch.setattr(
            snpseq_metadata.utilities, "find_samplesheet", self._return_samplesheet
        )

        runfolder_name = "this-is-a-runfolder-name"
        runfolder_path = os.path.join(
            "/this", "is", "a", "runfolder", "path", runfolder_name
        )
        samplesheet_name = self._return_samplesheet()[0]
        fc = Flowcell(runfolder_path=runfolder_path)
        assert fc.samplesheet == samplesheet_name

        monkeypatch.setattr(
            snpseq_metadata.utilities, "find_samplesheet", self._return_alt_samplesheet
        )
        assert fc.samplesheet == samplesheet_name

    def test_get_experiments(self, monkeypatch):
        monkeypatch.setattr(
            snpseq_metadata.utilities,
            "parse_samplesheet_data",
            self._return_samplesheet_data,
        )

        runfolder_name = "this-is-a-runfolder-name"
        runfolder_path = os.path.join(
            "/this", "is", "a", "runfolder", "path", runfolder_name
        )
        samplesheet_name = "this-is-a-supplied-samplesheet"

        fc = Flowcell(runfolder_path=runfolder_path, samplesheet=samplesheet_name)
        experiments = fc.get_experiments()

        samplesheet_data = self._return_samplesheet_data()
        assert len(experiments) == len(
            list(set([row["description"] for row in samplesheet_data]))
        )
