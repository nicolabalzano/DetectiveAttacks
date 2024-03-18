from pprint import pprint

from src.Domain.container.AttackPatternsContainer import AttackPatternsContainer
from src.Domain.container.CampaignsContainer import CampaignsContainer
from src.Domain.container.ToolsMalwareContainer import ToolsMalwareContainer
from src.Domain.conversionFromMitreAttack.AttackPatternsRetriever import AttackPatternsRetriever
from src.Domain.conversionFromMitreAttack.CampaignsRetriever import CampaignsRetriever
from src.Domain.conversionFromMitreAttack.ToolsMalwareRetriever import ToolsMalwareRetriever
from src.Domain.mitreAttackData.MitreAttackData import mitre_attack_data

attack_pattern_stix_id = "attack-pattern--57340c81-c025-4189-8fa0-fc7ede51bae4"
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

pprint(len(AttackPatternsContainer(AttackPatternsRetriever().get_all_objects()).get_data()))
pprint(len(CampaignsContainer(CampaignsRetriever().get_all_objects()).get_data()))
pprint(len(ToolsMalwareContainer(ToolsMalwareRetriever().get_all_objects()).get_data()))
# pprint(type(CampaignsContainer().get_data()[0].x_mitre_domains))
print(AttackPatternsContainer().get_data()[0])
# print(CampaignsContainer().get_data()[0].attack_patterns_and_relationships[0])
# print("\n\n")
# print(ToolsContainer().get_data()[0].attack_patterns_and_relationships[0])
# pprint(CampaignsContainer().get_data()[2])

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
