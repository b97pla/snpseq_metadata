import json
import os

from snpseq_metadata.models.ngi_models import NGIFlowcell
from snpseq_metadata.models.converter import Converter


runfolder_path = os.path.join("tests", "resources", "210415_A00001_0123_BXYZ321XY")
flowcell = NGIFlowcell(runfolder_path=runfolder_path)

# serialize the NGIFlowcell object to json
flowcell_json = flowcell.to_json()
json_out = f"{runfolder_path}.ngi.json"
with open(json_out, "w") as fh:
    json.dump(flowcell_json, fh, indent=2)

# transform the NGIFlowcell object to a SRARunSet object
run_set = Converter.ngi_to_sra(flowcell)

# serialize the flowcell object to json and dump to file
jsonobj = run_set.to_json()
json_out = f"{runfolder_path}.sra.json"
with open(json_out, "w") as fh:
    json.dump(jsonobj, fh, indent=2)

# serialize the flowcell object to XML and dump to file
xmlstr = run_set.to_xml()
xml_out = f"{runfolder_path}.sra.xml"
with open(xml_out, "w") as fh:
    fh.write(xmlstr)

# serialize the flowcell object to manifest and dump to file
manifest = run_set.to_manifest()
manifest_out = f"{runfolder_path}.sra.manifest"
with open(manifest_out, "w") as fh:
    for row in manifest:
        fh.write("\t".join(row))
        fh.write("\n")
