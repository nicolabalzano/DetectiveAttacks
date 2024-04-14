import nvdlib
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from wandb.wandb_torch import torch
import transformers

from src.domain.container.mySTIXContainer.AssetContainer import AssetContainer
from src.domain.container.mySTIXContainer.AttackPatternsContainer import AttackPatternsContainer
from src.domain.container.AttackToCVEContainer import AttackToCVEContainer
from src.domain.container.mySTIXContainer.CampaignsContainer import CampaignsContainer
from src.domain.container.mySTIXContainer.ToolsMalwareContainer import ToolsMalwareContainer
from src.domain.interfaceToMitre.conversionType.AttackToCVERetriever import AttackToCVERetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.AssetsRetriever import AssetRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.AttackPatternsRetriever import \
    AttackPatternsRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.CampaignsRetriever import CampaignsRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.ToolsMalwareRetriever import ToolsMalwareRetriever
from src.domain.interfaceToMitre.mitreData.FetchData import *
from src.domain.interfaceToMitre.mitreData.mitreAttackToCVE.SentenceSimilarityModel import SentenceSimilarityModel

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





# Check similarity for already mapped cve to search the min sim threshold 

for at_to_cve in AttackToCVEContainer().get_data()['mapping_objects']:
    # or at_to_cve['mapping_type'] == 'uncategorized'
    # and at_to_cve['capability_id'] == 'CVE-2020-15189'
    condition_met = False
    if at_to_cve['mapping_type'] == 'exploitation_technique' and condition_met:
        print(at_to_cve['capability_id'])

        new_mapping = {
            'cve_id': at_to_cve['capability_id'],

            'attack_object_id': at_to_cve['attack_object_id'],

            'attack_object_name': at_to_cve['attack_object_name'],

            'similarity': SentenceSimilarityModel().check_similarity(
                nvdlib.searchCVE(cveId=at_to_cve['capability_id'])[0].descriptions[0].value,
                AttackPatternsContainer().get_object_from_data_by_mitre_id(
                    at_to_cve['attack_object_id'].strip()).description)
        }

        data_extracted = read_from_json('..\\domain\\interfaceToMitre\\mitreData\\mitreAttackToCVE\\files\\',
                                        'attack_to_cve_ssm_sim_check')
        data_extracted['mapping'].append(new_mapping)
        save_to_json_file(data_extracted, 'attack_to_cve_ssm_sim_check',
                          '..\\domain\\interfaceToMitre\\mitreData\\mitreAttackToCVE\\files\\')

        if at_to_cve['mapping_type'] == 'exploitation_technique' and at_to_cve['capability_id'] == 'CVE-2020-15189':
            condition_met = True
