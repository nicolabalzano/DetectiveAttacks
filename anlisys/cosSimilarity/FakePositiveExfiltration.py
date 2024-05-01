# INITIALIZE DATA
from src.model.interfaceToMitre.mitreData.mitreAttackToCVE.SentenceSimilarityModelAPI import SentenceSimilarityModelAPI
import nvdlib
from src.model.container.mySTIXContainer.AssetContainer import AssetContainer
from src.model.container.mySTIXContainer.AttackPatternsContainer import AttackPatternsContainer
from src.model.container.AttackToCVEContainer import AttackToCVEContainer
from src.model.container.mySTIXContainer.CampaignsContainer import CampaignsContainer
from src.model.container.mySTIXContainer.ToolsMalwareContainer import ToolsMalwareContainer
from src.model.interfaceToMitre.conversionType.AttackToCVERetriever import AttackToCVERetriever
from src.model.interfaceToMitre.conversionType.stixConversionType.AssetsRetriever import AssetRetriever
from src.model.interfaceToMitre.conversionType.stixConversionType.AttackPatternsRetriever import \
    AttackPatternsRetriever
from src.model.interfaceToMitre.conversionType.stixConversionType.CampaignsRetriever import CampaignsRetriever
from src.model.interfaceToMitre.conversionType.stixConversionType.ToolsMalwareRetriever import ToolsMalwareRetriever
from src.model.interfaceToMitre.mitreData.FetchData import *

data_extracted = read_from_json('.\\files\\', 'attack_to_cve_ssm_sim_check')
data_extracted = data_extracted['mapping'][:-100]
print("Dataset dimension:", len(data_extracted))

"""
condition_met = False
    if at_to_cve['mapping_type'] == 'exploitation_technique' and condition_met:
        print(at_to_cve['capability_id'])
        
    if at_to_cve['mapping_type'] == 'exploitation_technique' and at_to_cve['capability_id'] == 'CVE-2020-15189':
        condition_met = True        
"""


def count_fake_positive(threshold: float):
    count = 0

    # Reduce to 50 CVE mapping
    for mapping in data_extracted:
        print(mapping['cve_id'])
        counter = 0
        cve_desc = nvdlib.searchCVE(cveId=mapping['cve_id'])[0].descriptions[0].value
        for at in AttackPatternsContainer().get_data():
            # if attack pattern is not in the mapping check if is a fake positive
            counter += 1
            print("*", counter)
            if at.x_mitre_id not in [mitre_id for mitre_id in data_extracted]:
                sim = SentenceSimilarityModelAPI().check_similarity(cve_desc, at.description)
                if sim >= threshold:
                    count += 1
                    new_mapping = {
                        'cve_id': mapping['cve_id'],

                        'cve_desc': cve_desc,

                        'attack_object_id': at.x_mitre_id,

                        'attack_object_name': at.name,

                        'similarity': sim
                    }
                    data_extracted_fp = read_from_json('.\\files\\', 'fake_positive')
                    data_extracted_fp['mapping'].append(new_mapping)
                    save_to_json_file(data_extracted_fp, 'fake_positive', '.\\files\\')
    print("Fake Positive:", count)
    return count


count_fake_positive(0.5)
