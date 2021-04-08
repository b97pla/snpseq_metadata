import os

from typing import Dict

import snpseq_metadata.utilities


class ResultFile:
    def __init__(
        self,
        filepath: str,
        filetype: str,
        checksum: str = None,
        checksum_method: str = None,
    ) -> None:
        self.filepath = filepath
        self.filetype = filetype
        if checksum is not None:
            self.checksum = checksum
        self.checksum_method = checksum_method or "MD5"

    def __getattr__(self, item) -> str:
        if item == "checksum":
            self.checksum = snpseq_metadata.utilities.calculate_checksum_from_file(
                queryfile=self.filepath, method=self.checksum_method
            )
        return getattr(self, item)

    def __eq__(self, other) -> bool:
        return (
            os.path.normpath(self.filepath) == os.path.normpath(other.filepath)
            and self.filetype == other.filetype
            and self.checksum == other.checksum
            and self.checksum_method == other.checksum_method
        )

    def to_json(self) -> Dict[str, str]:
        return {
            "@filename": self.filepath,
            "@filetype": self.filetype,
            "@checksum": self.checksum,
            "@checksum_method": self.checksum_method,
        }


class FastqFile(ResultFile):
    def __init__(
        self, filepath: str, checksum: str = None, checksum_method: str = None
    ) -> None:
        super(FastqFile, self).__init__(
            filepath=filepath,
            filetype="fastq",
            checksum=checksum,
            checksum_method=checksum_method,
        )
