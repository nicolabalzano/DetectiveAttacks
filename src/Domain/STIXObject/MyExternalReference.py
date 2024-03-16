from dataclasses import dataclass


@dataclass
class MyExternalReference:
    source_name: str
    url: str
    external_id: str = None
    description: str = None