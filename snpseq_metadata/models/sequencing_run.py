from typing import Any, Dict, List, TypeVar, Union

from snpseq_metadata.models.experiment import ExperimentRef
from snpseq_metadata.models.file_models import FastqFile

J = TypeVar("J", str, Dict[str, Any], List[Any])


class SequencingRun:
    def __init__(
        self,
        run_alias: str,
        run_center: str = None,
        experiment_ref: ExperimentRef = None,
        fastqfiles: List[FastqFile] = None,
    ) -> None:
        self.run_alias = run_alias
        self.run_center = run_center
        self.experiment_ref = experiment_ref
        self.fastqfiles = fastqfiles or []

    def to_json(
        self,
    ) -> Dict[str, J]:
        return {
            "@alias": self.run_alias,
            "@run_center": self.run_center,
            "EXPERIMENT_REF": self.experiment_ref.to_json()
            if self.experiment_ref
            else {},
            "DATA_BLOCK": {
                "FILES": {"FILE": list(map(lambda f: f.to_json(), self.fastqfiles))}
            },
        }


class NGIUppsalaRun(SequencingRun):
    def __init__(
        self,
        run_alias: str,
        experiment_ref: ExperimentRef = None,
        fastqfiles: List[FastqFile] = None,
    ) -> None:
        super(NGIUppsalaRun, self).__init__(
            run_alias=run_alias,
            run_center="National Genomics Infrastructure, Uppsala",
            experiment_ref=experiment_ref,
            fastqfiles=fastqfiles,
        )
