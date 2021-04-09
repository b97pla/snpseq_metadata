from typing import Dict, List, Type, TypeVar, Optional

from snpseq_metadata.models.ngi_models.sequencing_platform import (
    NGIIlluminaSequencingPlatform,
)
from snpseq_metadata.models.ngi_models.library import NGILibrary
from snpseq_metadata.models.ngi_models.metadata_model import NGIMetadataModel
from snpseq_metadata.models.ngi_models.study import NGIStudyRef

T = TypeVar("T", bound="NGIExperiment")
TR = TypeVar("TR", bound="NGIExperimentRef")
TS = TypeVar("TS", bound="NGIExperimentSet")


class NGIExperimentRef(NGIMetadataModel):
    def __init__(self, experiment_name: str, project_id: str, sample_id: str) -> None:
        self.experiment_name = experiment_name
        self.project_id = project_id
        self.sample_id = sample_id

    @classmethod
    def from_samplesheet_row(
        cls: Type[TR], samplesheet_row: Dict, platform: NGIIlluminaSequencingPlatform
    ) -> TR:
        project_id = samplesheet_row.get("sample_project")
        sample_id = samplesheet_row.get("sample_id")
        experiment_name = f"{project_id}-{sample_id}-{platform.model_name}"
        return cls(
            experiment_name=experiment_name, project_id=project_id, sample_id=sample_id
        )

    @classmethod
    def from_json(cls: Type[TR], json_obj: Dict) -> TR:
        return cls(
            experiment_name=json_obj.get("experiment_name"),
            project_id=json_obj.get("project_id"),
            sample_id=json_obj.get("sample_id"),
        )

    def is_reference_to(self, other: T) -> bool:
        return isinstance(other, NGIExperiment) and self.experiment_name == other.alias


class NGIExperiment(NGIMetadataModel):
    def __init__(
        self,
        alias: str,
        title: str,
        project: NGIStudyRef,
        platform: NGIIlluminaSequencingPlatform,
        library: NGILibrary,
    ) -> None:
        self.alias = alias
        self.title = title
        self.project = project
        self.platform = platform
        self.library = library

    @classmethod
    def from_json(cls: Type[T], json_obj: Dict) -> T:
        project = NGIStudyRef.from_json(json_obj=json_obj.get("project"))
        platform = NGIIlluminaSequencingPlatform.from_json(
            json_obj=json_obj.get("platform")
        )
        library = NGILibrary.from_json(json_obj=json_obj.get("library"))
        return cls(
            alias=json_obj.get("alias"),
            title=json_obj.get("title"),
            project=project,
            platform=platform,
            library=library,
        )


class NGIExperimentSet(NGIMetadataModel):
    def __init__(self, experiments: List[NGIExperiment]) -> None:
        self.experiments = experiments

    @classmethod
    def from_json(cls: Type[TS], json_obj: Dict) -> TS:
        experiments = [
            NGIExperiment.from_json(exp) for exp in json_obj.get("experiments", [])
        ]
        return cls(experiments=experiments)

    def get_experiment_for_reference(
        self, experiment_ref: NGIExperimentRef
    ) -> Optional[NGIExperiment]:
        try:
            return next(
                filter(
                    lambda exp: experiment_ref.is_reference_to(exp), self.experiments
                )
            )
        except StopIteration:
            pass
