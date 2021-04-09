from typing import ClassVar, Tuple, Type, TypeVar

from snpseq_metadata.models.ngi_models import (
    NGIMetadataModel,
    NGISampleDescriptor,
    NGIStudyRef,
    NGIRun,
    NGIIlluminaSequencingPlatform,
    NGIFlowcell,
    NGIResultFile,
    NGIExperimentRef,
    NGIExperiment,
    NGIExperimentSet,
    NGILibrary,
)
from snpseq_metadata.models.sra_models import (
    SRAMetadataModel,
    SRASampleDescriptor,
    SRAStudyRef,
    SRARun,
    SRAIlluminaSequencingPlatform,
    SRARunSet,
    SRAResultFile,
    SRAExperimentRef,
    SRAExperiment,
    SRAExperimentSet,
    SRALibrary,
)
from snpseq_metadata.models.ngi_to_sra_library_mapping import (
    ApplicationSampleTypeMapping,
)
from snpseq_metadata.exceptions import LibraryStrategyNotRecognizedException

T = TypeVar("T", bound="Converter")


class Converter:
    @classmethod
    def ngi_to_sra(cls: Type[T], ngi_model: NGIMetadataModel) -> SRAMetadataModel:
        for subclass in cls.__subclasses__():
            if isinstance(ngi_model, subclass.ngi_model_class):
                return subclass.ngi_to_sra(ngi_model=ngi_model)


class ConvertSampleDescriptor(Converter):

    ngi_model_class: ClassVar[Type] = NGISampleDescriptor
    sra_model_class: ClassVar[Type] = SRASampleDescriptor

    @classmethod
    def ngi_to_sra(cls: Type[T], ngi_model: ngi_model_class) -> sra_model_class:
        return cls.sra_model_class.create_object(refname=ngi_model.sample_id)


class ConvertStudyRef(Converter):

    ngi_model_class: ClassVar[Type] = NGIStudyRef
    sra_model_class: ClassVar[Type] = SRAStudyRef

    @classmethod
    def ngi_to_sra(cls: Type[T], ngi_model: ngi_model_class) -> sra_model_class:
        return cls.sra_model_class.create_object(refname=ngi_model.project_id)


class ConvertRun(Converter):

    ngi_model_class: ClassVar[Type] = NGIRun
    sra_model_class: ClassVar[Type] = SRARun

    @classmethod
    def ngi_to_sra(cls: Type[T], ngi_model: ngi_model_class) -> sra_model_class:
        return cls.sra_model_class.create_object(
            run_alias=ngi_model.run_alias,
            run_date=ngi_model.run_date,
            experiment_ref=Converter.ngi_to_sra(ngi_model.experiment_ref),
            run_center=ngi_model.run_center,
            fastqfiles=[Converter.ngi_to_sra(n) for n in ngi_model.fastqfiles],
        )


class ConvertSequencingPlatform(Converter):

    ngi_model_class: ClassVar[Type] = NGIIlluminaSequencingPlatform
    sra_model_class: ClassVar[Type] = SRAIlluminaSequencingPlatform

    @classmethod
    def ngi_to_sra(cls: Type[T], ngi_model: ngi_model_class) -> sra_model_class:
        return cls.sra_model_class.create_object(model_name=ngi_model.model_name)


class ConvertRunSet(Converter):

    ngi_model_class: ClassVar[Type] = NGIFlowcell
    sra_model_class: ClassVar[Type] = SRARunSet

    @classmethod
    def ngi_to_sra(cls: Type[T], ngi_model: ngi_model_class) -> sra_model_class:
        return cls.sra_model_class.create_object(
            runs=[Converter.ngi_to_sra(f) for f in ngi_model.sequencing_runs]
        )


class ConvertResultFile(Converter):

    ngi_model_class: ClassVar[Type] = NGIResultFile
    sra_model_class: ClassVar[Type] = SRAResultFile

    @classmethod
    def ngi_to_sra(cls: Type[T], ngi_model: ngi_model_class) -> sra_model_class:
        return cls.sra_model_class.create_object(
            filepath=ngi_model.filepath,
            filetype=ngi_model.filetype,
            checksum=ngi_model.checksum,
            checksum_method=ngi_model.checksum_method,
        )


class ConvertExperimentRef(Converter):

    ngi_model_class: ClassVar[Type] = NGIExperimentRef
    sra_model_class: ClassVar[Type] = SRAExperimentRef

    @classmethod
    def ngi_to_sra(cls: Type[T], ngi_model: ngi_model_class) -> sra_model_class:
        return cls.sra_model_class.create_object(
            experiment_name=ngi_model.experiment_name
        )


class ConvertExperiment(Converter):

    ngi_model_class: ClassVar[Type] = NGIExperiment
    sra_model_class: ClassVar[Type] = SRAExperiment

    @classmethod
    def ngi_to_sra(cls: Type[T], ngi_model: ngi_model_class) -> sra_model_class:
        return cls.sra_model_class.create_object(
            alias=ngi_model.alias,
            title=ngi_model.title,
            study_ref=Converter.ngi_to_sra(ngi_model=ngi_model.project),
            platform=Converter.ngi_to_sra(ngi_model=ngi_model.platform),
            library=Converter.ngi_to_sra(ngi_model=ngi_model.library),
        )


class ConvertExperimentSet(Converter):

    ngi_model_class: ClassVar[Type] = NGIExperimentSet
    sra_model_class: ClassVar[Type] = SRAExperimentSet

    @classmethod
    def ngi_to_sra(cls: Type[T], ngi_model: ngi_model_class) -> sra_model_class:
        return cls.sra_model_class.create_object(
            experiments=[
                Converter.ngi_to_sra(ngi_experiment)
                for ngi_experiment in ngi_model.experiments
            ],
        )


class ConvertLibrary(Converter):

    ngi_model_class: ClassVar[Type] = NGILibrary
    sra_model_class: ClassVar[Type] = SRALibrary

    @classmethod
    def ngi_to_sra(cls: Type[T], ngi_model: ngi_model_class) -> sra_model_class:
        (
            library_selection,
            library_source,
            library_strategy,
        ) = cls.objects_from_application_info(
            application=ngi_model.application,
            sample_type=ngi_model.sample_type,
            library_kit=ngi_model.library_kit,
        )
        return cls.sra_model_class.create_object(
            sample=Converter.ngi_to_sra(ngi_model.sample),
            description=ngi_model.description,
            strategy=library_strategy,
            source=library_source,
            selection=library_selection,
            is_paired=ngi_model.is_paired,
        )

    @classmethod
    def objects_from_application_info(
        cls: Type[T], application: str, sample_type: str, library_kit: str
    ) -> Tuple[str, str, str]:
        mapping_obj = ApplicationSampleTypeMapping.create_object(
            application=application,
            sample_type=sample_type,
            sample_prep_kit=library_kit,
        )
        if not mapping_obj:
            raise LibraryStrategyNotRecognizedException(
                needle=f"{application}:{sample_type}:{library_kit}"
            )
        return (
            mapping_obj.sra_library_selection.name,
            mapping_obj.sra_library_source.name,
            mapping_obj.sra_library_strategy.name,
        )
