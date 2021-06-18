from typing import Dict, Type, TypeVar

from snpseq_metadata.models.metadata_model import MetadataModel

N = TypeVar("N", bound="NGIMetadataModel")


class NGIMetadataModel(MetadataModel):
    @classmethod
    def from_json(cls: Type[N], json_obj: Dict) -> N:
        raise NotImplementedError
