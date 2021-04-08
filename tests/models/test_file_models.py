import os

import snpseq_metadata.utilities
from snpseq_metadata.models.file_models import ResultFile, FastqFile


class TestResultFile:
    @staticmethod
    def _return_checksum(*args, **kwargs):
        return "this-is-a-calculated-checksum"

    @staticmethod
    def _return_alt_checksum(*args, **kwargs):
        return "this-is-another-calculated-checksum"

    def test___eq__(self):
        kwargs = {
            "filepath": os.path.join("/this", "is", "a", "path", "to", "a.file"),
            "filetype": "this-is-a-filetype",
            "checksum": "this-is-a-checksum",
            "checksum_method": "this-is-a-checksum-method",
        }
        obj_a = ResultFile(**kwargs)

        kwargs_b = kwargs.copy()
        kwargs_b["filepath"] = os.path.join(
            "/this", "is", "a", "..", "a", "path", "to", "a.file"
        )
        obj_b = ResultFile(**kwargs_b)

        assert obj_a == obj_b

        for kwarg in ["filepath", "filetype", "checksum", "checksum_method"]:
            kwargs_c = kwargs.copy()
            kwargs_c[kwarg] = "this-is-something-different"
            obj_c = ResultFile(**kwargs_c)

            assert obj_c != obj_a

    def test_to_json(self):
        filepath = os.path.join("/this", "is", "a", "path", "to", "a.file")
        filetype = "this-is-a-filetype"
        checksum = "this-is-a-checksum"
        checksum_method = "this-is-a-checksum-method"
        expected_json = {
            "@filename": filepath,
            "@filetype": filetype,
            "@checksum": checksum,
            "@checksum_method": checksum_method,
        }
        fileobj = ResultFile(
            filepath=filepath,
            filetype=filetype,
            checksum=checksum,
            checksum_method=checksum_method,
        )

        assert fileobj.to_json() == expected_json

    def test_checksum(self, monkeypatch):
        filepath = os.path.join("/this", "is", "a", "path", "to", "a.file")
        filetype = "this-is-a-filetype"
        checksum = "this-is-a-checksum"
        checksum_method = "this-is-a-checksum-method"
        calculated_checksum = self._return_checksum()

        monkeypatch.setattr(
            snpseq_metadata.utilities,
            "calculate_checksum_from_file",
            self._return_checksum,
        )

        # supplying a checksum when instantiating the file object should use that checksum
        fileobj = ResultFile(
            filepath=filepath,
            filetype=filetype,
            checksum=checksum,
            checksum_method=checksum_method,
        )

        assert fileobj.checksum == checksum

        # if a checksum is not provided, it should be calculated on first use
        fileobj = ResultFile(
            filepath=filepath,
            filetype=filetype,
            checksum_method=checksum_method,
        )
        assert fileobj.checksum == calculated_checksum

        # when a checksum has been calculated, it should be cached
        monkeypatch.setattr(
            snpseq_metadata.utilities,
            "calculate_checksum_from_file",
            self._return_alt_checksum,
        )
        assert fileobj.checksum == calculated_checksum


class TestFastqFile:
    def test_to_json(self):
        filepath = os.path.join("/this", "is", "a", "path", "to", "a.file")
        filetype = "fastq"
        checksum = "this-is-a-checksum"
        checksum_method = "this-is-a-checksum-method"
        expected_json = {
            "@filename": filepath,
            "@filetype": filetype,
            "@checksum": checksum,
            "@checksum_method": checksum_method,
        }
        fileobj = FastqFile(
            filepath=filepath,
            checksum=checksum,
            checksum_method=checksum_method,
        )

        assert fileobj.to_json() == expected_json
