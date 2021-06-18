from typing import ClassVar, Tuple, Type, TypeVar, Optional

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

from snpseq_metadata.models.lims_models import (
    LIMSSequencingContainer,
    LIMSSample,
    LIMSMetadataModel,
)
from snpseq_metadata.models.ngi_to_sra_library_mapping import (
    ApplicationSampleTypeMapping,
)
from snpseq_metadata.exceptions import LibraryStrategyNotRecognizedException

T = TypeVar("T", bound="Converter")


class Converter:

    ngi_model_class: ClassVar[Type] = NGIMetadataModel
    sra_model_class: ClassVar[Type] = SRAMetadataModel
    lims_model_class: ClassVar[Type] = LIMSMetadataModel

    @classmethod
    def ngi_to_sra(
        cls: Type[T], ngi_model: ngi_model_class
    ) -> Optional[sra_model_class]:
        # only recurse if this is called in the base class
        if cls == Converter:
            for subclass in cls.__subclasses__():
                if isinstance(ngi_model, subclass.ngi_model_class):
                    sra_model = subclass.ngi_to_sra(ngi_model=ngi_model)
                    if sra_model:
                        return sra_model

    @classmethod
    def lims_to_ngi(
        cls: Type[T], lims_model: lims_model_class
    ) -> Optional[ngi_model_class]:
        # only recurse if this is called in the base class
        if cls == Converter:
            for subclass in cls.__subclasses__():
                if isinstance(lims_model, subclass.lims_model_class):
                    ngi_model = subclass.lims_to_ngi(lims_model=lims_model)
                    if ngi_model:
                        return ngi_model


class ConvertSampleDescriptor(Converter):

    ngi_model_class = NGISampleDescriptor
    sra_model_class = SRASampleDescriptor
    lims_model_class = LIMSSample

    @classmethod
    def ngi_to_sra(
        cls: Type[T], ngi_model: ngi_model_class
    ) -> Optional[sra_model_class]:
        if ngi_model:
            return cls.sra_model_class.create_object(refname=ngi_model.sample_id)

    @classmethod
    def lims_to_ngi(
        cls: Type[T], lims_model: lims_model_class
    ) -> Optional[ngi_model_class]:
        if lims_model:
            return cls.ngi_model_class(sample_id=lims_model.sample_id)


class ConvertStudyRef(Converter):

    ngi_model_class = NGIStudyRef
    sra_model_class = SRAStudyRef
    lims_model_class = LIMSSample

    @classmethod
    def ngi_to_sra(
        cls: Type[T], ngi_model: ngi_model_class
    ) -> Optional[sra_model_class]:
        if ngi_model:
            return cls.sra_model_class.create_object(refname=ngi_model.project_id)

    @classmethod
    def lims_to_ngi(
        cls: Type[T], lims_model: lims_model_class
    ) -> Optional[ngi_model_class]:
        if lims_model:
            return cls.ngi_model_class(project_id=lims_model.project_id)


class ConvertRun(Converter):

    ngi_model_class = NGIRun
    sra_model_class = SRARun

    @classmethod
    def ngi_to_sra(
        cls: Type[T], ngi_model: ngi_model_class
    ) -> Optional[sra_model_class]:
        if ngi_model:
            return cls.sra_model_class.create_object(
                run_alias=ngi_model.run_alias,
                run_date=ngi_model.run_date,
                experiment=Converter.ngi_to_sra(ngi_model.experiment.get_reference()),
                run_center=ngi_model.run_center,
                fastqfiles=[
                    Converter.ngi_to_sra(n) for n in ngi_model.fastqfiles or []
                ],
            )


class ConvertSequencingPlatform(Converter):

    ngi_model_class = NGIIlluminaSequencingPlatform
    sra_model_class = SRAIlluminaSequencingPlatform
    lims_model_class = LIMSSample

    @classmethod
    def ngi_to_sra(
        cls: Type[T], ngi_model: ngi_model_class
    ) -> Optional[sra_model_class]:
        if ngi_model:
            return cls.sra_model_class.create_object(model_name=ngi_model.model_name)

    @classmethod
    def lims_to_ngi(
        cls: Type[T], lims_model: lims_model_class
    ) -> Optional[ngi_model_class]:
        if lims_model:
            return cls.ngi_model_class(
                model_name=lims_model.udf.get("udf_sequencing_instrument")
            )


class ConvertRunSet(Converter):

    ngi_model_class = NGIFlowcell
    sra_model_class = SRARunSet

    @classmethod
    def ngi_to_sra(
        cls: Type[T], ngi_model: ngi_model_class
    ) -> Optional[sra_model_class]:
        if ngi_model:
            return cls.sra_model_class.create_object(
                runs=[Converter.ngi_to_sra(f) for f in ngi_model.sequencing_runs or []]
            )


class ConvertResultFile(Converter):

    ngi_model_class = NGIResultFile
    sra_model_class = SRAResultFile

    @classmethod
    def ngi_to_sra(
        cls: Type[T], ngi_model: ngi_model_class
    ) -> Optional[sra_model_class]:
        if ngi_model:
            return cls.sra_model_class.create_object(
                filepath=ngi_model.filepath,
                filetype=ngi_model.filetype,
                checksum=ngi_model.checksum,
                checksum_method=ngi_model.checksum_method,
            )


class ConvertExperimentRef(Converter):

    ngi_model_class = NGIExperimentRef
    sra_model_class = SRAExperimentRef
    lims_model_class = LIMSSample

    @classmethod
    def ngi_to_sra(
        cls: Type[T], ngi_model: ngi_model_class
    ) -> Optional[sra_model_class]:
        if ngi_model:
            return cls.sra_model_class.create_object(experiment_name=ngi_model.alias)

    @classmethod
    def lims_to_ngi(
        cls: Type[T], lims_model: lims_model_class
    ) -> Optional[ngi_model_class]:
        if lims_model:
            sample = ConvertSampleDescriptor.lims_to_ngi(lims_model=lims_model)
            project = ConvertStudyRef.lims_to_ngi(lims_model=lims_model)
            platform = ConvertSequencingPlatform.lims_to_ngi(lims_model=lims_model)
            alias = f"{project.project_id}-{sample.sample_id}-{platform.model_name}"
            return cls.ngi_model_class(alias=alias, sample=sample, project=project)


class ConvertExperimentSet(Converter):

    ngi_model_class = NGIExperimentSet
    sra_model_class = SRAExperimentSet
    lims_model_class = LIMSSequencingContainer

    @classmethod
    def ngi_to_sra(
        cls: Type[T], ngi_model: ngi_model_class
    ) -> Optional[sra_model_class]:
        if ngi_model:
            return cls.sra_model_class.create_object(
                experiments=[
                    Converter.ngi_to_sra(ngi_experiment)
                    for ngi_experiment in ngi_model.experiments or []
                ],
            )

    @classmethod
    def lims_to_ngi(
        cls: Type[T], lims_model: lims_model_class
    ) -> Optional[ngi_model_class]:
        if lims_model:
            return cls.ngi_model_class(
                [
                    ConvertExperiment.lims_to_ngi(lims_model=lims_sample)
                    for lims_sample in lims_model.samples or []
                ]
            )


class ConvertLibrary(Converter):

    ngi_model_class = NGILibrary
    sra_model_class = SRALibrary
    lims_model_class = LIMSSample

    @classmethod
    def ngi_to_sra(
        cls: Type[T], ngi_model: ngi_model_class
    ) -> Optional[sra_model_class]:
        if ngi_model:
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
    def lims_to_ngi(
        cls: Type[T], lims_model: lims_model_class
    ) -> Optional[ngi_model_class]:
        if lims_model:
            sample = ConvertSampleDescriptor.lims_to_ngi(lims_model=lims_model)
            application = lims_model.udf.get("udf_application")
            sample_type = lims_model.udf.get("udf_sample_type")
            library_kit = lims_model.udf.get("udf_library_preparation_kit")
            description = (
                f"{sample.sample_id} - {application} - {sample_type} - {library_kit}"
            )
            is_paired = (
                True
                if lims_model.udf.get("udf_read_length", "").endswith("x2")
                else None
            )
            return cls.ngi_model_class(
                sample=sample,
                description=description,
                application=application,
                sample_type=sample_type,
                library_kit=library_kit,
                is_paired=is_paired,
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


class ConvertExperiment(Converter):

    ngi_model_class = NGIExperiment
    sra_model_class = SRAExperiment
    lims_model_class = LIMSSample

    @classmethod
    def ngi_to_sra(
        cls: Type[T], ngi_model: ngi_model_class
    ) -> Optional[sra_model_class]:
        if ngi_model:
            return cls.sra_model_class.create_object(
                alias=ngi_model.alias,
                title=ngi_model.title,
                study_ref=Converter.ngi_to_sra(ngi_model=ngi_model.project),
                platform=Converter.ngi_to_sra(ngi_model=ngi_model.platform),
                library=Converter.ngi_to_sra(ngi_model=ngi_model.library),
            )

    @classmethod
    def lims_to_ngi(
        cls: Type[T], lims_model: lims_model_class
    ) -> Optional[ngi_model_class]:
        if lims_model:
            sample = ConvertSampleDescriptor.lims_to_ngi(lims_model=lims_model)
            project = ConvertStudyRef.lims_to_ngi(lims_model=lims_model)
            platform = ConvertSequencingPlatform.lims_to_ngi(lims_model=lims_model)
            alias = f"{project.project_id}-{sample.sample_id}-{platform.model_name}"
            library = ConvertLibrary.lims_to_ngi(lims_model=lims_model)
            title = f"{project.project_id} - {library.description}"
            return cls.ngi_model_class(
                alias=alias,
                title=title,
                project=project,
                platform=platform,
                library=library,
            )
