from typing import Dict


class Library:
    def __init__(
        self,
        name: str,
        strategy: str,
        source: str,
        selection: str,
        paired_layout: bool = True,
        protocol: str = None,
    ) -> None:
        self.name = name
        self.strategy = strategy
        self.source = source
        self.selection = selection
        self.paired_layout = paired_layout
        self.protocol = protocol

    def to_json(self) -> Dict[str, str]:
        json_obj = {
            "LIBRARY_NAME": self.name,
            "LIBRARY_STRATEGY": self.strategy,
            "LIBRARY_SOURCE": self.source,
            "LIBRARY_SELECTION": self.selection,
            "LIBRARY_LAYOUT": {"PAIRED" if self.paired_layout else "SINGLE"},
        }
        if self.protocol:
            json_obj["LIBRARY_CONSTRUCTION_PROTOCOL"] = self.protocol
        return json_obj
