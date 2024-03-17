from pprint import pprint

from src.Domain.Container.AttackPatternsContainer import AttackPatternsContainer
from src.Domain.Container.CampaignsContainer import CampaignsContainer
from src.Domain.Container.ToolsContainer import ToolsContainer
from src.Domain.ConversionFromMitreAttack.AttackPatternsRetriever import AttackPatternsRetriever
from src.Domain.ConversionFromMitreAttack.CampaignsRetriever import CampaignsRetriever
from src.Domain.ConversionFromMitreAttack.ToolsRetriever import ToolsRetriever
from src.Domain.MitreAttackData.MitreAttackData import mitre_attack_data

attack_pattern_stix_id = "attack-pattern--57340c81-c025-4189-8fa0-fc7ede51bae4"

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
# pprint(len(ToolsContainer(ToolsRetriever().get_all_objects()).get_data()))
# pprint(type(CampaignsContainer().get_data()[0].x_mitre_domains))
# pprint(AttackPatternsContainer().get_data()[0])
print(CampaignsContainer().get_data()[1].attack_patterns_and_relationships[0])
#pprint(CampaignsContainer().get_data()[2])


# test see relationship type
'''
list_attack_id = [x.id for x in mitre_attack_data.get_techniques()]
pprint(list_attack_id)

for id_att in list_attack_id:
    list_obj = mitre_attack_data.get_software_using_technique(id_att)
    for l in list_obj:
        pprint(len(l['relationships']))
        # pprint(len(l['relationships']), l['relationships'][0].relationship_type)
'''

'''
pprint(mitre_attack_data.get_software_using_technique(attack_pattern_stix_id)[0]['relationships'])
'''
