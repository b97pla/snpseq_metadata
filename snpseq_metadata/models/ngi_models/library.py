from typing import Dict, Optional, Type, TypeVar

from snpseq_metadata.models.ngi_models.metadata_model import NGIMetadataModel
from snpseq_metadata.models.ngi_models.sample import NGISampleDescriptor

T = TypeVar("T", bound="NGILibrary")


class NGILibrary(NGIMetadataModel):
    def __init__(
        self,
        sample: NGISampleDescriptor,
        description: str,
        application: str,
        sample_type: str,
        library_kit: str,
        is_paired: Optional[bool] = None,
    ) -> None:
        self.sample = sample
        self.description = description
        self.application = application
        self.sample_type = sample_type
        self.library_kit = library_kit
        self.is_paired = is_paired

    @classmethod
    def from_json(cls: Type[T], json_obj: Dict) -> T:
        sample = NGISampleDescriptor.from_json(json_obj=json_obj.get("sample"))
        description = json_obj.get("description")
        sample_type = json_obj.get("sample_type")
        application = json_obj.get("application")
        library_kit = json_obj.get("library_kit")
        is_paired = json_obj.get("is_paired")
        return cls(
            sample=sample,
            description=description,
            sample_type=sample_type,
            application=application,
            library_kit=library_kit,
            is_paired=is_paired,
        )
