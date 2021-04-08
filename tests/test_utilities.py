import os
import pytest

from snpseq_metadata.exceptions import SampleSheetNotFoundException
import snpseq_metadata.utilities


def test_calculate_checksum_from_file():
    for testfile in filter(lambda f: f.endswith(".md5"), os.listdir("resources")):
        checksum = testfile.split(".")[0]
        method = "MD5"
        assert (
            snpseq_metadata.utilities.calculate_checksum_from_file(
                queryfile=os.path.join("resources", testfile), method=method
            )
            == checksum
        )


def test_parse_samplesheet_data():
    samplesheet = os.path.join(".", "resources", "test_samplesheet.csv")
    expected_rows = 38
    expected_fields = [
        "lane",
        "sample_id",
        "sample_name",
        "sample_plate",
        "sample_well",
        "i7_index_id",
        "index",
        "i5_index_id",
        "index2",
        "sample_project",
        "description",
    ]
    expected_projects = ["AB-2755", "AB-2769"]
    expected_samples_per_lane = {1: 6, 2: 6, 3: 13, 4: 13}

    samplesheet_data = snpseq_metadata.utilities.parse_samplesheet_data(samplesheet)
    assert len(samplesheet_data) == expected_rows
    assert sorted(list(samplesheet_data[0].keys())) == sorted(expected_fields)
    assert sorted(list(set([d["sample_project"] for d in samplesheet_data]))) == sorted(
        expected_projects
    )

    samples_per_lane = {
        lane: len(list(filter(lambda d: d["lane"] == str(lane), samplesheet_data)))
        for lane in range(1, 5)
    }
    assert samples_per_lane == expected_samples_per_lane


def test_find_samplesheet(monkeypatch):
    def _listdir_no_samplesheet(*args):
        return ["file1", "file2", "file3"]

    def _listdir_one_samplesheet(*args):
        return ["file1", "file2_SampleSheet.csv", "file3"]

    def _listdir_two_samplesheet(*args):
        return ["file1", "samplesheet.csv", "file2_SampleSheet.csv"]

    runfolder = os.path.join("this", "is", "a", "runfolder")

    # assert that finding no samplesheet raises an exception
    monkeypatch.setattr(os, "listdir", _listdir_no_samplesheet)
    with pytest.raises(SampleSheetNotFoundException):
        snpseq_metadata.utilities.find_samplesheet(runfolder)

    # assert that the expected samplesheet can be found
    monkeypatch.setattr(os, "listdir", _listdir_one_samplesheet)
    assert snpseq_metadata.utilities.find_samplesheet(runfolder) == [
        _listdir_one_samplesheet()[1]
    ]

    # assert that all samplesheets are returned when multiple are present
    monkeypatch.setattr(os, "listdir", _listdir_two_samplesheet)
    assert (
        snpseq_metadata.utilities.find_samplesheet(runfolder)
        == _listdir_two_samplesheet()[1:]
    )

    # assert that a supplied suffix is used
    assert snpseq_metadata.utilities.find_samplesheet(runfolder, suffix="e1") == [
        _listdir_two_samplesheet()[0]
    ]


def test_find_existing_samplesheet():
    # assert that an existing samplesheet can be found on disk
    runfolder = os.path.join(".", "resources")
    assert snpseq_metadata.utilities.find_samplesheet(runfolder) == [
        "test_samplesheet.csv"
    ]


def test_lookup_checksum_from_file():
    runfolder = os.path.join(".", "resources")
    checksumfile = os.path.join(runfolder, "MD5", "checksums.md5")

    # if a checksum file is missing, the method will throw an exception
    with pytest.raises(OSError):
        snpseq_metadata.utilities.lookup_checksum_from_file(
            checksumfile="this-file-does-not-exist", querypath="does-not-matter"
        )

    # for files having checksums in a file, assert that they can be retrieved
    for testfile in filter(lambda f: f.endswith(".md5"), os.listdir(runfolder)):
        expected_checksum = testfile.split(".")[0]
        queryfile = os.path.join(runfolder, testfile)
        querypath = os.path.relpath(queryfile, os.path.dirname(runfolder))
        observed_checksum = snpseq_metadata.utilities.lookup_checksum_from_file(
            checksumfile=checksumfile, querypath=querypath
        )
        assert observed_checksum == expected_checksum
