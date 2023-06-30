import dataclasses
from typing import ClassVar, Optional, Type, TypeVar, List, Tuple

from snpseq_metadata.models.xsdata import PlatformType, TypeIlluminaModel
from snpseq_metadata.models.sra_models.metadata_model import SRAMetadataModel
from snpseq_metadata.exceptions import InstrumentModelNotRecognizedException

T = TypeVar("T", "SRASequencingPlatform", "SRAIlluminaSequencingPlatform")


class SRASequencingPlatform(SRAMetadataModel):
    model_object_class: ClassVar[Type] = PlatformType

    def __getattr__(self, item) -> Optional[str]:
        try:
            if item in ("platform", "instrument_model"):
                field = next(
                    filter(
                        lambda x: getattr(self.model_object, x.name),
                        dataclasses.fields(self.model_object)))
                if item == "platform":
                    return field.metadata["name"]
                return getattr(self.model_object, field.name).instrument_model.value
        except StopIteration:
            pass

    @classmethod
    def create_object(cls: Type[T], model_name: str) -> T:
        raise NotImplementedError

    def to_manifest(self) -> List[Tuple[str, str]]:
        raise NotImplementedError


class SRAIlluminaSequencingPlatform(SRASequencingPlatform):

    @classmethod
    def object_from_name(cls: Type[T], model_name: str) -> TypeIlluminaModel:
        model_dict = {
            "novaseqx": TypeIlluminaModel.ILLUMINA_NOVA_SEQ_X,
            "novaseq": TypeIlluminaModel.ILLUMINA_NOVA_SEQ_6000,
            "miseq": TypeIlluminaModel.ILLUMINA_MI_SEQ,
            "iseq": TypeIlluminaModel.ILLUMINA_I_SEQ_100,
            "hiseqx": TypeIlluminaModel.HI_SEQ_X_TEN,
            "hiseq2500": TypeIlluminaModel.ILLUMINA_HI_SEQ_2500,
            "hiseq": TypeIlluminaModel.ILLUMINA_HI_SEQ_2000,
            "nextseq": TypeIlluminaModel.NEXT_SEQ_500,
            "": TypeIlluminaModel.UNSPECIFIED,
        }
        return cls._object_from_something(
            needle=model_name or "",
            haystack=model_dict,
            on_error=InstrumentModelNotRecognizedException,
        )

    @classmethod
    def create_object(cls: Type[T], model_name: str) -> T:
        model_object = PlatformType(
            illumina=PlatformType.Illumina(
                instrument_model=cls.object_from_name(model_name)
            )
        )
        return cls(model_object=model_object)

    def to_manifest(self) -> List[Tuple[str, str]]:
        manifest = [
            ("PLATFORM", self.platform),
            ("INSTRUMENT", self.instrument_model)
        ]
        return manifest
