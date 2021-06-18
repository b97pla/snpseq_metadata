import os
import json

from snpseq_metadata.models.ngi_models import (
    NGIStudyRef,
    NGISampleDescriptor,
    NGILibrary,
    NGIIlluminaSequencingPlatform,
    NGIExperiment,
    NGIExperimentSet,
)
from snpseq_metadata.models.converter import Converter


experiment_data = [
    {
        "project_id": "AB-1234",
        "sample_id": "AB-1234-SampleA-1",
        "application": "WG Re-Seq",
        "sample_type": "gDNA",
        "library_kit": "TruSeq DNA PCR-free Sample Preparation kit HT",
        "is_paired": True,
        "model_name": "NovaSeq",
    },
    {
        "project_id": "AB-1234",
        "sample_id": "AB-1234-SampleB-2",
        "application": "WG Re-Seq",
        "sample_type": "gDNA",
        "library_kit": "TruSeq DNA PCR-free Sample Preparation kit HT",
        "is_paired": True,
        "model_name": "NovaSeq",
    },
    {
        "project_id": "[PROJECT IDENTIFIER]",
        "sample_id": "[SAMPLE IDENTIFIER]",
        "application": "[SEQUENCING APPLICATION]",
        "sample_type": "[SAMPLE TYPE]",
        "library_kit": "[LIBRARY KIT]",
        "is_paired": "[True/False]",
        "model_name": "[INSTRUMENT MODEL]",
    },
]

experiments = []
for data in experiment_data:
    description = f'{data["sample_id"]} - {data["application"]} - {data["sample_type"]} - {data["library_kit"]}'
    title = f'{data["project_id"]} - {description}'
    alias = f'{data["project_id"]}-{data["sample_id"]}-{data["model_name"]}'

    project = NGIStudyRef(project_id=data["project_id"])
    sample = NGISampleDescriptor(sample_id=data["sample_id"])
    library = NGILibrary(
        sample=sample,
        description=description,
        application=data["application"],
        sample_type=data["sample_type"],
        library_kit=data["library_kit"],
        is_paired=data["is_paired"],
    )
    platform = NGIIlluminaSequencingPlatform(model_name=data["model_name"])
    experiment = NGIExperiment(
        alias=alias,
        title=title,
        project=project,
        library=library,
        platform=platform,
    )
    experiments.append(experiment)

experiment_set = NGIExperimentSet(experiments=experiments)

# serialize the NGIExperimentSet object to json
experiment_file = os.path.join("tests", "resources", "experiment")
json_out = f"{experiment_file}.ngi.json"
with open(json_out, "w") as fh:
    json.dump(experiment_set.to_json(), fh, indent=2)

# transform the NGIExperimentSet object to a SRAExperimentSet object
# remove the last experiment since it only contained annotations
experiment_set = NGIExperimentSet(experiments=experiments[0:2])
sra_experiment_set = Converter.ngi_to_sra(experiment_set)

# serialize the sra_experiment_set object to json and dump to file
json_out = f"{experiment_file}.sra.json"
with open(json_out, "w") as fh:
    json.dump(sra_experiment_set.to_json(), fh, indent=2)

# serialize the sra_experiment_set object to XML and dump to file
xmlstr = sra_experiment_set.to_xml()
xml_out = f"{experiment_file}.sra.xml"
with open(xml_out, "w") as fh:
    fh.write(xmlstr)

# serialize the sra_experiment_set object to manifest and dump to file
manifest = sra_experiment_set.to_manifest()
manifest_out = f"{experiment_file}.sra.manifest"
with open(manifest_out, "w") as fh:
    for row in manifest:
        fh.write("\t".join(row))
        fh.write("\n")
