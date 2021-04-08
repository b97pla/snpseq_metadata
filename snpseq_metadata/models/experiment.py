from typing import Dict, TypeVar

T = TypeVar("T", bound="Experiment")


class Experiment:
    def __init__(
        self, experiment_name: str, sample_project: str, sample_id: str, **kwargs: str
    ) -> None:
        self.experiment_name = experiment_name
        self.sample_project = sample_project
        self.sample_id = sample_id
        for field, value in kwargs.items():
            setattr(self, field.lower(), value)

    def __eq__(self, other) -> bool:
        return self.experiment_name == other.experiment_name

    def __str__(self) -> str:
        return self.experiment_name

    def to_json(self) -> Dict[str, str]:
        return {"@refname": self.experiment_name}

    @classmethod
    def from_samplesheet_row(cls, samplesheet_row: Dict[str, str]) -> T:
        experiment_name = samplesheet_row["description"].split(":")[-1]
        return Experiment(
            experiment_name=experiment_name,
            **{k: v for k, v in samplesheet_row.items()}
        )
