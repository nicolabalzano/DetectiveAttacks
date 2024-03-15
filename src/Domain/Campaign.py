from dataclasses import dataclass, field
from typing import List, Optional

from stix2.v20 import Campaign, ExternalReference


@dataclass
class MyExternalReference:
    source_name: str
    url: str
    external_id: str = None
    description: str = None

@dataclass
class MyCampaign:
    type: str
    id: str
    created_by_ref: str
    created: str
    modified: str
    name: str
    description: str
    x_mitre_version: str
    revoked: bool
    x_mitre_attack_spec_version: str
    x_mitre_deprecated: bool
    aliases: List[str] = field(default_factory=list)
    external_references: List[ExternalReference] = field(default_factory=list)
    x_mitre_contributors: List[str] = field(default_factory=list)
    x_mitre_domains: List[str] = field(default_factory=list)
    # first_seen: str
    # last_seen: str
    # object_marking_refs: field(default_factory=List[str])
    # x_mitre_first_seen_citation: str
    # x_mitre_last_seen_citation: str
    # x_mitre_modified_by_ref: str

    @staticmethod
    def del_unused_attr(campaign: Campaign):
        campaign_dict = campaign.__dict__
        campaign_dict_data = campaign_dict['_inner']

        chiavi_da_eliminare = [
            'first_seen',
            'last_seen',
            'object_marking_refs',
            'x_mitre_first_seen_citation',
            'x_mitre_last_seen_citation',
            'x_mitre_modified_by_ref'
        ]

        for chiave in chiavi_da_eliminare:
            if chiave in campaign_dict_data:
                del campaign_dict_data[chiave]

        return campaign_dict_data

