import json
from pprint import pprint

from mitreattack.stix20 import MitreAttackData

from src.Domain.Campaign import MyCampaign, ExternalReference, MyExternalReference
from src.Domain.JSONEncoder import MyJSONEncoder
from src.Domain.TechniquesRetriver import TechniquesRetriver

mitre_attack_data = MitreAttackData("enterprise-attack.json")

# TEST SINGLE CAMPAIGN INITIALIZE
'''
technique_stix_id = "attack-pattern--7e150503-88e7-4861-866b-ff1ac82c4475"

campaign = TechniquesRetriver.get_object_by_techniques_id(technique_stix_id, mitre_attack_data)[0]["object"]

MyCampaign.del_unused_attr(campaign)
my_campaign = MyCampaign(**campaign)

print(my_campaign.external_references)
pprint(my_campaign)
'''

# TEST MULTIPLE CAMPAIGN INITIALIZE
for techniques in mitre_attack_data.get_techniques():
    for campaign in TechniquesRetriver.get_object_by_techniques_id(techniques['id'], mitre_attack_data):
        c = campaign["object"]
        #print(json.dumps(c.__dict__, indent=2, cls=MyJSONEncoder))
    
        MyCampaign.del_unused_attr(c)
        my_campaign = MyCampaign(**c)
        pprint(my_campaign.name)
