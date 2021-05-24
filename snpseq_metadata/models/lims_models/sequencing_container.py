from typing import Dict, List, Type, TypeVar

from snpseq_metadata.models.lims_models.metadata_model import LIMSMetadataModel
from snpseq_metadata.models.lims_models.sample import LIMSSample

L = TypeVar("L", bound="LIMSSequencingContainer")


class LIMSSequencingContainer(LIMSMetadataModel):
    def __init__(self, name: str, samples: List[LIMSSample]):
        self.name = name
        self.samples = samples

    @classmethod
    def from_json(cls: Type[L], json_obj: Dict) -> L:
        name = json_obj.get("name")
        samples = [
            LIMSSample.from_json(json_obj=sample_json)
            for sample_json in json_obj.get("samples", [])
        ]
        return cls(name=name, samples=samples)
