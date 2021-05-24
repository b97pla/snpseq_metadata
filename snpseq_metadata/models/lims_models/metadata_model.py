from typing import Dict, Type, TypeVar

from snpseq_metadata.models.metadata_model import MetadataModel

L = TypeVar("L", bound="LIMSMetadataModel")


class LIMSMetadataModel(MetadataModel):
    @classmethod
    def from_json(cls: Type[L], json_obj: Dict) -> L:
        raise NotImplementedError
