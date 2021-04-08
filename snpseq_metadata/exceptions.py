import os


class SampleSheetNotFoundException(Exception):
    def __init__(self, runfolder: str) -> None:
        self.message = f"No samplesheet found in {os.path.basename(runfolder)}"


class NoSampleSheetDataFoundException(Exception):
    def __init__(self, samplesheet: str) -> None:
        self.message = f"No data could be parsed from {os.path.join(os.path.basename(os.path.dirname(samplesheet)), os.path.basename(samplesheet))}"
