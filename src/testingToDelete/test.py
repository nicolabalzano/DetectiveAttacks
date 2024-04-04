from pprint import pprint

from src.domain.container.AssetContainer import AssetContainer
from src.domain.container.AttackPatternsContainer import AttackPatternsContainer
from src.domain.container.AttackToCVEContainer import AttackToCVEContainer
from src.domain.container.CampaignsContainer import CampaignsContainer
from src.domain.container.ToolsMalwareContainer import ToolsMalwareContainer
from src.domain.interfaceToMitre.conversionType.stixConversionType.AssetsRetriever import AssetRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.AttackPatternsRetriever import AttackPatternsRetriever
from src.domain.interfaceToMitre.conversionType.AttackToCVERetriever import AttackToCVERetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.CampaignsRetriever import CampaignsRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.ToolsMalwareRetriever import ToolsMalwareRetriever
from src.domain.interfaceToMitre.mitreData.FetchData import fetch_enterprise_data, fetch_mobile_data, \
    fetch_ics_data, fetch_atlas_data, fetch_attack_to_cve_data
from src.domain.interfaceToMitre.mitreData.mitreAttackToCVE.AttackBert import AttackBert

# fetch data
fetch_enterprise_data()
fetch_mobile_data()
fetch_ics_data()
fetch_atlas_data()
fetch_attack_to_cve_data()

# init language semantic model
AttackBert()

# attack_pattern_stix_id = "attack-pattern--57340c81-c025-4189-8fa0-fc7ede51bae4"
# attack_pattern_name = "Drive-by Compromise"
campaign_stix_id = "campaign--b4e5a4a9-f3be-4631-ba8f-da6ebb067fac"
tool_malware_stix_id = "tool--b76b2d94-60e4-4107-a903-4a3a7622fb3b"

# get all tools
'''
retrieverTools = RetrieverTools()
pprint(len(retrieverTools.get_all_objects()))
'''

# get all campaigns
'''
retrieverCampaigns = RetrieverCampaigns()
pprint(len(retrieverCampaigns.get_all_objects()))
'''

# technique
'''
pprint(len(mitre_attack_data.get_techniques(remove_revoked_deprecated=True)))
pprint(mitre_attack_data.get_techniques()[0])
'''

# get all techniques
'''
retrieverAttackPatterns = AttackPatternsRetriever()
pprint(len(retrieverAttackPatterns.get_all_objects()))
'''

# container

print("dimension AttackPatternsContainer",
      len(AttackPatternsContainer(AttackPatternsRetriever().get_all_objects()).get_data()))
print("dimension CampaignsContainer", len(CampaignsContainer(CampaignsRetriever().get_all_objects()).get_data()))
print("dimension ToolsMalwareContainer", len(ToolsMalwareContainer(ToolsMalwareRetriever().get_all_objects()).get_data()))
print("dimension AssetContainer", len(AssetContainer(AssetRetriever().get_all_objects()).get_data()))
print("dimension AttackToCVEContainer", len(AttackToCVEContainer(AttackToCVERetriever().get_all_objects()).get_data()))

# print(len(AttackPatternsContainer().get_object_from_data_by_id('attack-pattern--25852363-5968-4673-b81d-341d5ed90bd1').assets_and_relationship))

"""
for ats in AttackPatternsContainer().get_object_from_data_by_name("Destruction"):
    print(ats.name)
"""

# pprint(type(CampaignsContainer().get_data()[0].x_mitre_domains))
# print(AttackPatternsContainer().get_data()[0])
# print(CampaignsContainer().get_data()[0].attack_patterns_and_relationships[0])
# print("\n\n")
# print(ToolsContainer().get_data()[0].attack_patterns_and_relationships[0])
# pprint(CampaignsContainer().get_data()[2])

attack_pattern_stix_id = AttackPatternsContainer().get_object_from_data_by_name('External Remote Services')[0].id

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
pprint(AttackToCVEContainer().get_attack_pattern_by_cve_id('CVE-2024-3151'))

"""
for at in AttackToCVEContainer().get_attack_pattern_by_cve_id('CVE-2024-3151')["Primary Impact"]:
    print(AttackPatternsContainer().get_object_from_data_by_mitre_id(at).x_mitre_id)
for at in AttackToCVEContainer().get_attack_pattern_by_cve_id('CVE-2024-3151')["Secondary Impact"]:
    print(AttackPatternsContainer().get_object_from_data_by_mitre_id(at).x_mitre_id)
for at in AttackToCVEContainer().get_attack_pattern_by_cve_id('CVE-2024-3151')["Exploitation Technique"]:
    print(AttackPatternsContainer().get_object_from_data_by_mitre_id(at).x_mitre_id)
for at in AttackToCVEContainer().get_attack_pattern_by_cve_id('CVE-2024-3151')["Uncategorized"]:
    print(AttackPatternsContainer().get_object_from_data_by_mitre_id(at).x_mitre_id)
"""

print("\nSearch cve id by attack pattern stix id:")
print(AttackToCVEContainer().get_cve_id_by_attack_pattern_mitre_id(
    AttackPatternsContainer().get_object_from_data_by_mitre_id('T1565.002').x_mitre_id
))

print("\n\nPhase and Domain of attack-pattern searched: ",
      AttackPatternsContainer().get_object_from_data_by_id(attack_pattern_stix_id).kill_chain_phases,
      AttackPatternsContainer().get_object_from_data_by_id(attack_pattern_stix_id).x_mitre_domains)

# lista per contare da quale matrice provengono le relazioni
i = 0


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
        if 'enterprise-attack' in at_rel_key.x_mitre_domains:
            enterprise.append(i)
        elif 'ics-attack' in at_rel_key.x_mitre_domains:
            ics.append(i)
        elif 'mobile-attack' in at_rel_key.x_mitre_domains:
            mobile.append(i)
        elif 'atlas-attack' in at_rel_key.x_mitre_domains:
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
        if 'enterprise-attack' in at_rel_key.x_mitre_domains:
            enterprise.append(i)
        elif 'ics-attack' in at_rel_key.x_mitre_domains:
            ics.append(i)
        elif 'mobile-attack' in at_rel_key.x_mitre_domains:
            mobile.append(i)
        elif 'atlas-attack' in at_rel_key.x_mitre_domains:
            atlas.append(i)
        i += 1

    print("   e", len(enterprise), "  m", len(mobile), "  i", len(ics), "  a", len(atlas), "\n")

# print(dict_probably_happened['evasion'])

'''
for att in attack_set:
    print(att.name)
'''

# get attack_patterns name from Campaign
'''
print(f"\n* Campaign {campaign_stix_id} related attack patterns:")
for attack_patterns_and_relationships_dict in CampaignsContainer().get_object_from_data_by_id(campaign_stix_id).attack_patterns_and_relationships:
    for chiave in attack_patterns_and_relationships_dict:
        print(chiave.name)

# get attack_patterns name from ToolMalware
print(f"\n* ToolsMalware {tool_malware_stix_id} related attack patterns:")
for attack_patterns_and_relationships_dict in ToolsMalwareContainer().get_object_from_data_by_id(tool_malware_stix_id).attack_patterns_and_relationships:
    for chiave in attack_patterns_and_relationships_dict:
        print(chiave.name)
'''

# test see relationship type
'''
list_attack_id = [x.id for x in mitre_attack_data.get_techniques()]

for id_att in list_attack_id:
    list_obj = mitre_attack_data.get_techniques_used_by_campaign(id_att)
    for l in list_obj:
        pprint(len(l['relationships']))
        # pprint(len(l['relationships']), l['relationships'][0].relationship_type)
pprint(mitre_attack_data.get_techniques_used_by_campaign(campaign_stix_id)[0]['relationships'])
'''

'''
pprint(mitre_attack_data.get_software_using_technique(attack_pattern_stix_id)[0]['relationships'])
'''
