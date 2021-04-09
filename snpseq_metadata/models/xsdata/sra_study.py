from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from snpseq_metadata.models.xsdata.sra_common import (
    AttributeType,
    LinkType,
    ObjectType,
    XrefType,
)


class StudyTypeExistingStudyType(Enum):
    """
    :cvar WHOLE_GENOME_SEQUENCING: Sequencing of a single organism.
    :cvar METAGENOMICS: Sequencing of a community.
    :cvar TRANSCRIPTOME_ANALYSIS: Sequencing and characterization of
        transcription elements.
    :cvar RESEQUENCING: Sequencing of a sample with respect to a
        reference.
    :cvar EPIGENETICS: Cellular differentiation study.
    :cvar SYNTHETIC_GENOMICS: Sequencing of modified, synthetic, or
        transplanted genomes.
    :cvar FORENSIC_OR_PALEO_GENOMICS: Sequencing of recovered genomic
        material.
    :cvar GENE_REGULATION_STUDY: Study of gene expression regulation.
    :cvar CANCER_GENOMICS: Study of cancer genomics.
    :cvar POPULATION_GENOMICS: Study of populations and evolution
        through genomics.
    :cvar RNASEQ: RNA sequencing study.
    :cvar EXOME_SEQUENCING: The study investigates the exons of the
        genome.
    :cvar POOLED_CLONE_SEQUENCING: The study is sequencing clone pools
        (BACs, fosmids, other constructs).
    :cvar TRANSCRIPTOME_SEQUENCING: Sequencing of transcription
        elements.
    :cvar OTHER: Study type not listed.
    """

    WHOLE_GENOME_SEQUENCING = "Whole Genome Sequencing"
    METAGENOMICS = "Metagenomics"
    TRANSCRIPTOME_ANALYSIS = "Transcriptome Analysis"
    RESEQUENCING = "Resequencing"
    EPIGENETICS = "Epigenetics"
    SYNTHETIC_GENOMICS = "Synthetic Genomics"
    FORENSIC_OR_PALEO_GENOMICS = "Forensic or Paleo-genomics"
    GENE_REGULATION_STUDY = "Gene Regulation Study"
    CANCER_GENOMICS = "Cancer Genomics"
    POPULATION_GENOMICS = "Population Genomics"
    RNASEQ = "RNASeq"
    EXOME_SEQUENCING = "Exome Sequencing"
    POOLED_CLONE_SEQUENCING = "Pooled Clone Sequencing"
    TRANSCRIPTOME_SEQUENCING = "Transcriptome Sequencing"
    OTHER = "Other"


@dataclass
class StudyType(ObjectType):
    """A Study is a container for a sequencing investigation that may comprise
    multiple experiments.

    The Study has an overall goal, but is otherwise minimally defined in
    the SRA. A Study is composed of a descriptor, zero or more
    experiments, and zero or more analyses. The submitter may decorate
    the Study with web links and properties.

    :ivar descriptor:
    :ivar study_links: Links to resources related to this study
        (publication, datasets, online databases).
    :ivar study_attributes: Properties and attributes of the study.
        These can be entered as free-form  tag-value pairs. For certain
        studies, submitters may be asked to follow a community
        established ontology when describing the work.
    """

    descriptor: Optional["StudyType.Descriptor"] = field(
        default=None,
        metadata={
            "name": "DESCRIPTOR",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    study_links: Optional["StudyType.StudyLinks"] = field(
        default=None,
        metadata={
            "name": "STUDY_LINKS",
            "type": "Element",
            "namespace": "",
        },
    )
    study_attributes: Optional["StudyType.StudyAttributes"] = field(
        default=None,
        metadata={
            "name": "STUDY_ATTRIBUTES",
            "type": "Element",
            "namespace": "",
        },
    )

    @dataclass
    class Descriptor:
        """
        :ivar study_title: Title of the study as would be used in a
            publication.
        :ivar study_type: The STUDY_TYPE presents a controlled
            vocabulary for expressing the overall purpose of the study.
        :ivar study_abstract: Briefly describes the goals, purpose, and
            scope of the Study.  This need not be listed if it can be
            inherited from a referenced publication.
        :ivar center_name: DEPRECATED.  Use STUDY@center_name instead.
            Controlled vocabulary identifying the sequencing center,
            core facility, consortium, or laboratory responsible for the
            study.
        :ivar center_project_name: Submitter defined project name.  This
            field is intended for backward tracking of the study record
            to the submitter's LIMS.
        :ivar project_id: DEPRECATED (use RELATED_STUDIES.STUDY
            instead).   The required PROJECT_ID accession is generated
            by the Genome Project database at NCBI  and will be valid
            also at the other archival institutions.
        :ivar related_studies:
        :ivar study_description: More extensive free-form description of
            the study.
        """

        study_title: Optional[str] = field(
            default=None,
            metadata={
                "name": "STUDY_TITLE",
                "type": "Element",
                "namespace": "",
            },
        )
        study_type: Optional["StudyType.Descriptor.StudyType"] = field(
            default=None,
            metadata={
                "name": "STUDY_TYPE",
                "type": "Element",
                "namespace": "",
            },
        )
        study_abstract: Optional[str] = field(
            default=None,
            metadata={
                "name": "STUDY_ABSTRACT",
                "type": "Element",
                "namespace": "",
            },
        )
        center_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "CENTER_NAME",
                "type": "Element",
                "namespace": "",
            },
        )
        center_project_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "CENTER_PROJECT_NAME",
                "type": "Element",
                "namespace": "",
            },
        )
        project_id: Optional[int] = field(
            default=None,
            metadata={
                "name": "PROJECT_ID",
                "type": "Element",
                "namespace": "",
            },
        )
        related_studies: Optional["StudyType.Descriptor.RelatedStudies"] = field(
            default=None,
            metadata={
                "name": "RELATED_STUDIES",
                "type": "Element",
                "namespace": "",
            },
        )
        study_description: Optional[str] = field(
            default=None,
            metadata={
                "name": "STUDY_DESCRIPTION",
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class StudyType:
            """
            :ivar existing_study_type:
            :ivar new_study_type: To propose a new term, select Other
                and enter a new study type.
            """

            existing_study_type: Optional[StudyTypeExistingStudyType] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )
            new_study_type: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

        @dataclass
        class RelatedStudies:
            related_study: List[
                "StudyType.Descriptor.RelatedStudies.RelatedStudy"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "RELATED_STUDY",
                    "type": "Element",
                    "namespace": "",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class RelatedStudy:
                """
                :ivar related_link: Related study or project record from
                    a list of supported databases. The study's
                    information is derived from this project record
                    rather than stored as first class information.
                :ivar is_primary: Whether this study object is
                    designated as the primary source of the study or
                    project information.
                """

                related_link: Optional[XrefType] = field(
                    default=None,
                    metadata={
                        "name": "RELATED_LINK",
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                is_primary: Optional[bool] = field(
                    default=None,
                    metadata={
                        "name": "IS_PRIMARY",
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )

    @dataclass
    class StudyLinks:
        study_link: List[LinkType] = field(
            default_factory=list,
            metadata={
                "name": "STUDY_LINK",
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
            },
        )

    @dataclass
    class StudyAttributes:
        study_attribute: List[AttributeType] = field(
            default_factory=list,
            metadata={
                "name": "STUDY_ATTRIBUTE",
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
            },
        )


@dataclass
class Study(StudyType):
    class Meta:
        name = "STUDY"


@dataclass
class StudySetType:
    study: List[StudyType] = field(
        default_factory=list,
        metadata={
            "name": "STUDY",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )


@dataclass
class StudySet(StudySetType):
    """
    An STUDY_SET is a container for a set of studies and a common namespace.
    """

    class Meta:
        name = "STUDY_SET"
