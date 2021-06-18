import json

from snpseq_metadata.models.lims_models import LIMSSequencingContainer
from snpseq_metadata.models.converter import Converter


class TestLIMSModel:
    def test_parse_json(self, lims_json_obj):
        container = LIMSSequencingContainer.from_json(json_obj=lims_json_obj)
        assert container.name == "HKV5JAAAA"
        assert len(container.samples) == 9
        print(json.dumps(container.to_json(), indent=2))

    def test_to_ngi(self, lims_json_obj):
        container = LIMSSequencingContainer.from_json(json_obj=lims_json_obj)
        experiment_set = Converter.lims_to_ngi(lims_model=container)
        print(json.dumps(experiment_set.to_json(), indent=2))

    def test_to_sra(self, lims_json_obj):
        container = LIMSSequencingContainer.from_json(json_obj=lims_json_obj)
        experiment_set = Converter.lims_to_ngi(lims_model=container)
        sra_experiments = Converter.ngi_to_sra(ngi_model=experiment_set)
        print(json.dumps(sra_experiments.to_json(), indent=2))
