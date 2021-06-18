from dataclasses import dataclass, field
from typing import List, Optional
from snpseq_metadata.models.xsdata.sra_common import (
    AttributeType,
    LinkType,
    ObjectType,
)


@dataclass
class SampleType(ObjectType):
    """A Sample defines an isolate of sequenceable material upon which
    sequencing experiments can be based.

    The Sample object may be a surrogate for taxonomy accession or an
    anonymized individual identifier.  Or, it may fully specify
    provenance and isolation method of the starting material.

    :ivar title: Short text that can be used to call out sample records
        in search results or in displays.
    :ivar sample_name:
    :ivar description: Free-form text describing the sample, its origin,
        and its method of isolation.
    :ivar sample_links: Links to resources related to this sample or
        sample set (publication, datasets, online databases).
    :ivar sample_attributes: Properties and attributes of a sample.
        These can be entered as free-form  tag-value pairs. For certain
        studies, submitters may be asked to follow a community
        established ontology when describing the work.
    """

    title: Optional[str] = field(
        default=None,
        metadata={
            "name": "TITLE",
            "type": "Element",
            "namespace": "",
        },
    )
    sample_name: Optional["SampleType.SampleName"] = field(
        default=None,
        metadata={
            "name": "SAMPLE_NAME",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "DESCRIPTION",
            "type": "Element",
            "namespace": "",
        },
    )
    sample_links: Optional["SampleType.SampleLinks"] = field(
        default=None,
        metadata={
            "name": "SAMPLE_LINKS",
            "type": "Element",
            "namespace": "",
        },
    )
    sample_attributes: Optional["SampleType.SampleAttributes"] = field(
        default=None,
        metadata={
            "name": "SAMPLE_ATTRIBUTES",
            "type": "Element",
            "namespace": "",
        },
    )

    @dataclass
    class SampleName:
        """
        :ivar taxon_id: NCBI Taxonomy Identifier.  This is appropriate
            for individual organisms and some environmental samples.
        :ivar scientific_name: Scientific name of sample that
            distinguishes its taxonomy.  Please use a  name or synonym
            that is tracked in the INSDC Taxonomy database.  Also, this
            field can be used to confirm the TAXON_ID setting.
        :ivar common_name: GenBank common name of the organism.
            Examples: human, mouse.
        :ivar display_name:
        """

        taxon_id: Optional[int] = field(
            default=None,
            metadata={
                "name": "TAXON_ID",
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        scientific_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "SCIENTIFIC_NAME",
                "type": "Element",
                "namespace": "",
            },
        )
        common_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "COMMON_NAME",
                "type": "Element",
                "namespace": "",
            },
        )
        display_name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass
    class SampleLinks:
        sample_link: List[LinkType] = field(
            default_factory=list,
            metadata={
                "name": "SAMPLE_LINK",
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
            },
        )

    @dataclass
    class SampleAttributes:
        sample_attribute: List[AttributeType] = field(
            default_factory=list,
            metadata={
                "name": "SAMPLE_ATTRIBUTE",
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
            },
        )


@dataclass
class Sample(SampleType):
    class Meta:
        name = "SAMPLE"


@dataclass
class SampleSetType:
    sample: List[SampleType] = field(
        default_factory=list,
        metadata={
            "name": "SAMPLE",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )


@dataclass
class SampleSet(SampleSetType):
    """
    SAMPLE_SET serves as a container for a set of samples and a name space for
    establishing referential integrity between them.
    """

    class Meta:
        name = "SAMPLE_SET"
