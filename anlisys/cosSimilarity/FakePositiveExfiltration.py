# INITIALIZE DATA
from src.domain.interfaceToMitre.mitreData.mitreAttackToCVE.SentenceSimilarityModel import SentenceSimilarityModel
import nvdlib
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

data_extracted = read_from_json('.\\files\\', 'attack_to_cve_ssm_sim_check')
data_extracted = data_extracted['mapping'][:-100]
print("Dataset dimension:", len(data_extracted))


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
                sim = SentenceSimilarityModel().check_similarity(cve_desc, at.description)
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
