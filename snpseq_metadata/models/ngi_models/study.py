from typing import Dict, Type, TypeVar

from snpseq_metadata.models.ngi_models.metadata_model import NGIMetadataModel

T = TypeVar("T", bound="NGIStudyRef")


class NGIStudyRef(NGIMetadataModel):
    def __init__(self, project_id: str) -> None:
        self.project_id = project_id

    @classmethod
    def from_json(cls: Type[T], json_obj: Dict) -> T:
        return cls(project_id=json_obj.get("project_id"))
