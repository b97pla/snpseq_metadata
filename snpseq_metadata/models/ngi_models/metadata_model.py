from typing import Dict, Iterable, Type, TypeVar, Union
import datetime

from snpseq_metadata.models.metadata_model import MetadataModel

N = TypeVar("N", bound="NGIMetadataModel")
T = TypeVar("T")


class NGIMetadataModel(MetadataModel):
    @classmethod
    def from_json(cls: Type[N], json_obj: Dict) -> N:
        raise NotImplementedError(
            f"{str(cls)} does not implement creating object from json"
        )

    def to_json(self) -> Dict:
        json_obj = {}
        for name, value in vars(self).items():
            json_obj[name] = self._item_to_json(value)
        return json_obj

    @classmethod
    def _item_to_json(cls: Type[N], item: T) -> Union[T, Dict, Iterable]:
        if isinstance(item, NGIMetadataModel):
            return item.to_json()
        if isinstance(item, dict):
            return {k: cls._item_to_json(v) for k, v in item.items()}
        if isinstance(item, str):
            return item
        if isinstance(item, Iterable):
            return [cls._item_to_json(i) for i in item]
        if isinstance(item, datetime.datetime):
            return item.isoformat(" ")
        return item

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and all(
            map(
                lambda k: getattr(other, k, None) == getattr(self, k, None),
                vars(self).keys(),
            )
        )
