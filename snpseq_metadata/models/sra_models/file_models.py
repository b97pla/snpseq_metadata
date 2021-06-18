import os

from typing import ClassVar, TypeVar, Type, List, Tuple

from snpseq_metadata.models.sra_models.metadata_model import SRAMetadataModel
from snpseq_metadata.models.xsdata import Run, FileFiletype, FileChecksumMethod
from snpseq_metadata.exceptions import (
    ChecksumMethodNotRecognizedException,
    FiletypeNotRecognizedException,
)

T = TypeVar("T", bound="SRAResultFile")


class SRAResultFile(SRAMetadataModel):
    model_object_class: ClassVar[Type] = Run.DataBlock.Files.File

    def __eq__(self, other: T) -> bool:
        return (
            os.path.normpath(self.model_object.filename)
            == os.path.normpath(other.model_object.filename)
            and self.model_object.filetype == other.model_object.filetype
            and self.model_object.checksum == other.model_object.checksum
            and self.model_object.checksum_method == other.model_object.checksum_method
        )

    @classmethod
    def object_from_method(cls: Type[T], checksum_method: str) -> FileChecksumMethod:
        method_dict = {method.value.lower(): method for method in FileChecksumMethod}
        return cls._object_from_something(
            checksum_method, method_dict, ChecksumMethodNotRecognizedException
        )

    @classmethod
    def object_from_filetype(cls: Type[T], filetype: str) -> FileFiletype:
        filetype_dict = {filetype.value.lower(): filetype for filetype in FileFiletype}
        return cls._object_from_something(
            filetype, filetype_dict, FiletypeNotRecognizedException
        )

    @classmethod
    def create_object(
        cls: Type[T],
        filepath: str,
        filetype: str,
        checksum: str,
        checksum_method: str = "MD5",
    ) -> T:
        xsd_checksum_method = cls.object_from_method(checksum_method)
        xsd_filetype = cls.object_from_filetype(filetype)
        model_object = Run.DataBlock.Files.File(
            filename=filepath,
            filetype=xsd_filetype,
            checksum=checksum,
            checksum_method=xsd_checksum_method,
        )
        return cls(model_object=model_object)

    def to_manifest(self) -> List[Tuple[str, str]]:
        return [(self.model_object.filetype.name, self.model_object.filename)]


class SRAFastqFile(SRAResultFile):
    pass
