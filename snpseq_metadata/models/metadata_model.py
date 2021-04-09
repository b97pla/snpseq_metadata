from typing import Dict, TypeVar, Type
from snpseq_metadata.exceptions import SomethingNotRecognizedException

T = TypeVar("T")


class MetadataModel:
    def to_json(self) -> Dict:
        raise NotImplementedError(
            f"{type(self).__name__} does not implement exporting object to json"
        )

    @staticmethod
    def _object_from_something(
        needle: str,
        haystack: Dict[str, T],
        on_error: Type[SomethingNotRecognizedException],
    ) -> T:
        try:
            return haystack[needle.lower()]
        except KeyError:
            on_error(needle, list(haystack.keys()))
