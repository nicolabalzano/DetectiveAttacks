from pprint import pprint

from src.Domain.Container.AttackPatternsContainer import AttackPatternsContainer
from src.Domain.Container.CampaignsContainer import CampaignsContainer
from src.Domain.Container.ToolsContainer import ToolsContainer
from src.Domain.Conversion.AttackPatternsRetriever import AttackPatternsRetriever
from src.Domain.Conversion.CampaignsRetriever import CampaignsRetriever
from src.Domain.Conversion.ToolsRetriever import ToolsRetriever
from src.Domain.MitreAttackData.MitreAttackData import mitre_attack_data

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

pprint(len(CampaignsContainer(tuple(CampaignsRetriever().get_all_objects())).get_data()))
pprint(len(ToolsContainer(tuple(ToolsRetriever().get_all_objects())).get_data()))
pprint(len(AttackPatternsContainer(tuple(AttackPatternsRetriever().get_all_objects())).get_data()))
pprint(AttackPatternsContainer().get_data()[0])
pprint(AttackPatternsContainer().get_data()[1])
pprint(AttackPatternsContainer().get_data()[2])


# _get_objects_using_technique_id
#attack_pattern_stix_id = "attack-pattern--57340c81-c025-4189-8fa0-fc7ede51bae4"

