from dataclasses import dataclass, field
from pprint import pprint
from typing import List

from stix2.v20 import Tool

from src.Domain.STIXObject.AbstractMySTIXObject import AbstractMySTIXObject


@dataclass
class MyTool(AbstractMySTIXObject):
    labels: tuple[str] = field(default_factory=tuple)
    x_mitre_platforms: tuple[str] = field(default_factory=tuple)
    # x_mitre_modified_by_ref: str
    # object_marking_refs: List[str] = field(default_factory=list)
    # x_mitre_aliases: List[str] = field(default_factory=list)