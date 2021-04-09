from typing import ClassVar, Type, TypeVar, List, Tuple

from snpseq_metadata.models.sra_models.metadata_model import SRAMetadataModel
from snpseq_metadata.models.xsdata import Experiment as XSDExperiment

T = TypeVar("T", bound="SRAStudyRef")


class SRAStudyRef(SRAMetadataModel):

    model_object_class: ClassVar[Type] = XSDExperiment.StudyRef

    @classmethod
    def create_object(cls: Type[T], refname: str) -> T:
        model_object = XSDExperiment.StudyRef(refname=refname)
        return cls(model_object=model_object)

    def to_manifest(self) -> List[Tuple[str, str]]:
        return [("STUDY", self.model_object.refname)]
