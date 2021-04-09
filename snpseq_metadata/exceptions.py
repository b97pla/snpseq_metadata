import os

from typing import List, Optional


class FastqFileLocationNotFoundException(Exception):
    def __init__(self, sample_project: str, sample_id: str, search_path: str) -> None:
        self.message = f"No FASTQ file location found in {search_path} for {sample_project} and {sample_id}"


class RunParametersNotFoundException(Exception):
    def __init__(self, runfolder: str) -> None:
        self.message = f"No RunParameters found in {os.path.basename(runfolder)}"


class SampleSheetNotFoundException(Exception):
    def __init__(self, runfolder: str) -> None:
        self.message = f"No samplesheet found in {os.path.basename(runfolder)}"


class NoSampleSheetDataFoundException(Exception):
    def __init__(self, samplesheet: str) -> None:
        self.message = f"No data could be parsed from {os.path.join(os.path.basename(os.path.dirname(samplesheet)), os.path.basename(samplesheet))}"


class SomethingNotRecognizedException(Exception):
    thing = "Needle"
    things = "needles"

    def __init__(self, needle: str, haystack: Optional[List[str]] = None):
        haystack_str = f" ({', '.join(haystack)})" if haystack else ""
        self.message = f"{self.thing} '{needle}' was not in the list of recognized {self.things}{haystack_str}"


class InstrumentModelNotRecognizedException(SomethingNotRecognizedException):
    thing = "Instrument model"
    things = "models"


class LibraryStrategyNotRecognizedException(SomethingNotRecognizedException):
    thing = "Library strategy"
    things = "strategies"


class LibrarySourceNotRecognizedException(SomethingNotRecognizedException):
    thing = "Library source"
    things = "sources"


class LibrarySelectionNotRecognizedException(SomethingNotRecognizedException):
    thing = "Library selection"
    things = "selections"


class ChecksumMethodNotRecognizedException(SomethingNotRecognizedException):
    thing = "Checksum method"
    things = "methods"


class FiletypeNotRecognizedException(SomethingNotRecognizedException):
    thing = "File type"
    things = "file types"
