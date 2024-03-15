import json
from dataclasses import asdict
from datetime import datetime

from mitreattack import Technique
from mitreattack.stix20 import MitreAttackData
from stix2.v20 import AttackPattern

from src.Domain.JSONEncoder import DateTimeEncoder
from src.Domain.Technique import MyAttackPattern

mitre_attack_data = MitreAttackData("enterprise-attack.json")

# gruppo
groups = mitre_attack_data.get_groups_by_alias("Cozy Bear")

for group in groups:
    print(type(group))

# campagna
campaigns = mitre_attack_data.get_campaigns_by_alias("Frankenstein")

for campaign in campaigns:
    print(type(campaign))

# tecnica
techniques = mitre_attack_data.get_techniques_by_tactic("reconnaissance", "enterprise-attack")

for technique in techniques:
    print(type(technique))

my_full_attack_pattern = MyAttackPattern(
    id="attack-pattern-001",
    name="Example Attack Pattern",
    created_by_ref="organization-001",
    description="This is an example attack pattern.",
    kill_chain_phases=["reconnaissance", "delivery"],
    labels=["malware", "ransomware"],
    external_references=["https://example.com/reference1", "https://example.com/reference2"],
    object_marking_refs=["marking-definition-001"],
    granular_markings=["marking-001"]
)

print(json.dumps(asdict(my_full_attack_pattern), indent=2, cls=DateTimeEncoder))