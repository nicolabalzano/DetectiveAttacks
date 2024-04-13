from src.domain.container.AttackToCVEContainer import AttackToCVEContainer
from src.domain.container.mySTIXContainer.AssetContainer import AssetContainer
from src.domain.container.mySTIXContainer.AttackPatternsContainer import AttackPatternsContainer
from src.domain.container.mySTIXContainer.CampaignsContainer import CampaignsContainer
from src.domain.container.mySTIXContainer.ToolsMalwareContainer import ToolsMalwareContainer
from src.domain.interfaceToMitre.conversionType.AttackToCVERetriever import AttackToCVERetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.AssetsRetriever import AssetRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.AttackPatternsRetriever import \
    AttackPatternsRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.CampaignsRetriever import CampaignsRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.ToolsMalwareRetriever import ToolsMalwareRetriever
from src.domain.interfaceToMitre.mitreData.FetchData import *
from src.gptAPI.GPTRequest import gpt_request

fetch_enterprise_data()
fetch_mobile_data()
fetch_ics_data()
fetch_atlas_data()
fetch_attack_to_cve_data()

# container

print("\ndimension AttackPatternsContainer",
      len(AttackPatternsContainer(AttackPatternsRetriever().get_all_objects()).get_data()))
print("dimension CampaignsContainer", len(CampaignsContainer(CampaignsRetriever().get_all_objects()).get_data()))
print("dimension ToolsMalwareContainer",
      len(ToolsMalwareContainer(ToolsMalwareRetriever().get_all_objects()).get_data()))
print("dimension AssetContainer", len(AssetContainer(AssetRetriever().get_all_objects()).get_data()))
print("dimension AttackToCVEContainer", len(AttackToCVEContainer(AttackToCVERetriever().get_all_objects()).get_data()))

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

# gpt_request()
