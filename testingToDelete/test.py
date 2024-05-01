import nvdlib

from src.model.container.vulnerabilityContainer.MitreToCVEContainer import MitreToCVEContainer
from src.model.container.mySTIXContainer.AssetContainer import AssetContainer
from src.model.container.mySTIXContainer.AttackPatternsContainer import AttackPatternsContainer
from src.model.container.mySTIXContainer.CampaignsContainer import CampaignsContainer
from src.model.container.mySTIXContainer.ToolsMalwareContainer import ToolsMalwareContainer

campaign_stix_id = "campaign--b4e5a4a9-f3be-4631-ba8f-da6ebb067fac"
tool_malware_stix_id = "tool--b76b2d94-60e4-4107-a903-4a3a7622fb3b"



attack_pattern_stix_id = AttackPatternsContainer().get_object_from_data_by_mitre_id('T1053.005').id

# External Remote Services
print("\n\nName of searched attack:", attack_pattern_stix_id)

attack_set_by_campaign = CampaignsContainer().get_related_attack_patterns_by_attack_pattern_id(attack_pattern_stix_id)
attack_set_by_tool = ToolsMalwareContainer().get_related_attack_patterns_by_attack_pattern_id(attack_pattern_stix_id)
attack_set_by_asset = AssetContainer().get_related_attack_patterns_by_attack_pattern_id(attack_pattern_stix_id)
attack_set = AttackPatternsContainer().get_related_attack_patterns_by_attack_pattern_id(attack_pattern_stix_id)

print("\n* Related attacks: ")
print("By Campaigns", len(attack_set_by_campaign))
print("By ToolMalware", len(attack_set_by_tool))
print("By Asset", len(attack_set_by_asset))
print("--> By All", len(attack_set))

print("\nSearch AttackToCVE by cve id:")

# 'CVE-2024-3570', 'CVE-2024-3569', 'CVE-2024-3568',

for cve in ['CVE-2024-3388']:
    print("* ", cve)
    print("Description: ", nvdlib.searchCVE(cveId=cve)[0].descriptions[0].value)
    for key, value in MitreToCVEContainer().get_attack_pattern_by_vuln_id(cve).items():
        print("-", key)
        print([at_name.name for at_name in value])

print("\nSearch cve id by attack pattern mitre id:")
for dict_at in MitreToCVEContainer().get_vuln_id_by_attack_pattern_mitre_id(
        AttackPatternsContainer().get_object_from_data_by_name('Malicious File')[0].x_mitre_id):
    for key, value in dict_at.items():
        print(key)
        print(value)

print("\n\nPhase and model of attack-pattern searched: ",
      AttackPatternsContainer().get_object_from_data_by_id(attack_pattern_stix_id).kill_chain_phases,
      AttackPatternsContainer().get_object_from_data_by_id(attack_pattern_stix_id).x_mitre_domains)

i = 0
key_set = set()

print("\n* Probably happened attacks dict for phase: ")
dict_probably_happened = AttackPatternsContainer().get_probably_happened_attack_patterns_grouped_by_phase(
    AttackPatternsContainer().get_object_from_data_by_id(attack_pattern_stix_id))
for key in dict_probably_happened:
    print("  ", key, len(dict_probably_happened[key]))
    enterprise = []
    mobile = []
    ics = []
    atlas = []
    for at_rel_key in dict_probably_happened[key]:
        key_set.add(at_rel_key.x_mitre_id)
        if 'enterprise-attack' in at_rel_key.x_mitre_domains:
            enterprise.append(i)
        elif 'ics-attack' in at_rel_key.x_mitre_domains:
            ics.append(i)
        elif 'mobile-attack' in at_rel_key.x_mitre_domains:
            mobile.append(i)
        elif 'atlas' in at_rel_key.x_mitre_domains:
            atlas.append(i)
        i += 1

    print("   e", len(enterprise), "  m", len(mobile), "  i", len(ics), "  a", len(atlas), "\n")

print("\n* Probably futured attacks dict for phase: ")
dict_futured = AttackPatternsContainer().get_futured_attack_patterns_grouped_by_phase(
    AttackPatternsContainer().get_object_from_data_by_id(attack_pattern_stix_id))
for key in dict_futured:
    print("  ", key, len(dict_futured[key]))
    enterprise = []
    mobile = []
    ics = []
    atlas = []
    for at_rel_key in dict_futured[key]:
        print(at_rel_key.x_mitre_id)
        key_set.add(at_rel_key.x_mitre_id)
        if 'enterprise-attack' in at_rel_key.x_mitre_domains:
            enterprise.append(i)
        elif 'ics-attack' in at_rel_key.x_mitre_domains:
            ics.append(i)
        elif 'mobile-attack' in at_rel_key.x_mitre_domains:
            mobile.append(i)
        elif 'atlas' in at_rel_key.x_mitre_domains:
            atlas.append(i)
        i += 1

    print("   e", len(enterprise), "  m", len(mobile), "  i", len(ics), "  a", len(atlas), "\n")

print(key_set)

