from typing import Dict, Type, TypeVar

from snpseq_metadata.models.ngi_models.metadata_model import NGIMetadataModel

T = TypeVar("T", bound="NGISampleDescriptor")


class NGISampleDescriptor(NGIMetadataModel):
    def __init__(self, sample_id: str) -> None:
        self.sample_id = sample_id

    @classmethod
    def from_json(cls: Type[T], json_obj: Dict) -> T:
        return cls(sample_id=json_obj.get("sample_id"))
