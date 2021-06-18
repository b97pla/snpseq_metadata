import re
from typing import Dict, Type, TypeVar

from snpseq_metadata.models.ngi_models.metadata_model import NGIMetadataModel
from snpseq_metadata.exceptions import InstrumentModelNotRecognizedException

T = TypeVar("T", bound="NGISequencingPlatform")


class NGISequencingPlatform(NGIMetadataModel):
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    @classmethod
    def from_json(cls: Type[T], json_obj: Dict) -> T:
        return cls(model_name=json_obj.get("model_name"))


class NGIIlluminaSequencingPlatform(NGISequencingPlatform):
    @classmethod
    def model_name_from_id(cls: Type[T], id: str) -> str:
        m = re.match(r"^(\D+)\d+", id)
        model_prefix = m.group(1)
        model_dict = {
            "a": "NovaSeq",
            "m": "MiSeq",
            "fs": "iSeq",
            "st-e": "HiSeqX",
            "d": "HiSeq2500",
            "sn": "HiSeq",
        }
        return cls._object_from_something(
            needle=model_prefix,
            haystack=model_dict,
            on_error=InstrumentModelNotRecognizedException,
        )
