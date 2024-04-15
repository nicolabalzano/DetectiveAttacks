import nvdlib

from src.model.container.AttackToCVEContainer import AttackToCVEContainer
from src.model.container.mySTIXContainer.AssetContainer import AssetContainer
from src.model.container.mySTIXContainer.AttackPatternsContainer import AttackPatternsContainer
from src.model.container.mySTIXContainer.CampaignsContainer import CampaignsContainer
from src.model.container.mySTIXContainer.ToolsMalwareContainer import ToolsMalwareContainer
from src.model.interfaceToMitre.mitreData.FetchData import *
from anlisys.gptAPI.GPTRequest import gpt_request

# Extract
"""
at = AttackPatternsContainer().get_object_from_data_by_mitre_id('T1053.005')

dict_futured = AttackPatternsContainer().get_futured_attack_patterns_grouped_by_phase(at)

dict_probably_happened = AttackPatternsContainer().get_probably_happened_attack_patterns_grouped_by_phase(at)

combined_dict = {**dict_futured, **dict_probably_happened}

keys_set = set([at.x_mitre_id for ap_key, ats_value in combined_dict.items() for at in ats_value])

print(len(keys_set))
print(keys_set)

dict_id_name_and_description = {}
for mitre_id in keys_set:
    dict_id_name_and_description[mitre_id] = {
        "name": AttackPatternsContainer().get_object_from_data_by_mitre_id(mitre_id).name,
        "description": AttackPatternsContainer().get_object_from_data_by_mitre_id(mitre_id).description
    }

save_to_json_file(dict_id_name_and_description, "techniques_to_know", "./files/")

"""



