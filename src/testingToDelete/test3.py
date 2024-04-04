from pprint import pprint

import nvdlib

from src.domain.container.AssetContainer import AssetContainer
from src.domain.container.AttackPatternsContainer import AttackPatternsContainer
from src.domain.container.AttackToCVEContainer import AttackToCVEContainer
from src.domain.container.CampaignsContainer import CampaignsContainer
from src.domain.container.ToolsMalwareContainer import ToolsMalwareContainer
from src.domain.interfaceToMitre.conversionType.AttackToCVERetriever import AttackToCVERetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.AssetsRetriever import AssetRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.AttackPatternsRetriever import \
    AttackPatternsRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.CampaignsRetriever import CampaignsRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.ToolsMalwareRetriever import ToolsMalwareRetriever
from src.domain.interfaceToMitre.mitreData.FetchData import *
from src.domain.interfaceToMitre.mitreData.mitreAttackToCVE.AttackBert import AttackBert

fetch_enterprise_data()
fetch_mobile_data()
fetch_ics_data()
fetch_atlas_data()
fetch_attack_to_cve_data()

# container

print("dimension AttackPatternsContainer",
      len(AttackPatternsContainer(AttackPatternsRetriever().get_all_objects()).get_data()))
print("dimension CampaignsContainer", len(CampaignsContainer(CampaignsRetriever().get_all_objects()).get_data()))
print("dimension ToolsMalwareContainer",
      len(ToolsMalwareContainer(ToolsMalwareRetriever().get_all_objects()).get_data()))
print("dimension AssetContainer", len(AssetContainer(AssetRetriever().get_all_objects()).get_data()))
print("dimension AttackToCVEContainer", len(AttackToCVEContainer(AttackToCVERetriever().get_all_objects()).get_data()))

r = nvdlib.searchCVE(cveId='CVE-2024-30334')[0]
print(r.descriptions[0].value)
# pprint(r)

print([at.name for at in AttackToCVEContainer().get_attack_pattern_by_cve_id('CVE-2024-30334')])