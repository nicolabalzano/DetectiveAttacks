from src.domain.container.mySTIXContainer.AssetContainer import AssetContainer
from src.domain.container.mySTIXContainer.AttackPatternsContainer import AttackPatternsContainer
from src.domain.container.AttackToCVEContainer import AttackToCVEContainer
from src.domain.container.mySTIXContainer.CampaignsContainer import CampaignsContainer
from src.domain.container.mySTIXContainer.ToolsMalwareContainer import ToolsMalwareContainer
from src.domain.interfaceToMitre.conversionType.stixConversionType.AssetsRetriever import AssetRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.AttackPatternsRetriever import \
    AttackPatternsRetriever
from src.domain.interfaceToMitre.conversionType.AttackToCVERetriever import AttackToCVERetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.CampaignsRetriever import CampaignsRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.ToolsMalwareRetriever import ToolsMalwareRetriever
from src.domain.interfaceToMitre.mitreData.FetchData import fetch_enterprise_data, fetch_mobile_data, \
    fetch_ics_data, fetch_atlas_data, fetch_attack_to_cve_data
from src.domain.interfaceToMitre.mitreData.mitreAttackToCVE.AttackBert import AttackBert

# fetch data
fetch_enterprise_data()
fetch_mobile_data()
fetch_ics_data()
fetch_atlas_data()
fetch_attack_to_cve_data()

# init language semantic model
AttackBert()

# attack_pattern_stix_id = "attack-pattern--57340c81-c025-4189-8fa0-fc7ede51bae4"
# attack_pattern_name = "Drive-by Compromise"
campaign_stix_id = "campaign--b4e5a4a9-f3be-4631-ba8f-da6ebb067fac"
tool_malware_stix_id = "tool--b76b2d94-60e4-4107-a903-4a3a7622fb3b"

# container
print("\ndimension AttackPatternsContainer",
      len(AttackPatternsContainer(AttackPatternsRetriever().get_all_objects()).get_data()))
print("dimension CampaignsContainer", len(CampaignsContainer(CampaignsRetriever().get_all_objects()).get_data()))
print("dimension ToolsMalwareContainer",
      len(ToolsMalwareContainer(ToolsMalwareRetriever().get_all_objects()).get_data()))
print("dimension AssetContainer", len(AssetContainer(AssetRetriever().get_all_objects()).get_data()))
print("dimension AttackToCVEContainer", len(AttackToCVEContainer(AttackToCVERetriever().get_all_objects()).get_data()))

                                                                                                                            # External Remote Services
print("\n\nName of searched attack", AttackPatternsContainer().get_object_from_data_by_name('LLM Plugin Compromise')[0].name)
attack_pattern_stix_id = AttackPatternsContainer().get_object_from_data_by_name('LLM Plugin Compromise')[0].id

attack_set_by_campaign = CampaignsContainer().get_related_attack_patterns_by_attack_pattern_id(attack_pattern_stix_id)
attack_set_by_tool = ToolsMalwareContainer().get_related_attack_patterns_by_attack_pattern_id(attack_pattern_stix_id)
attack_set_by_asset = AssetContainer().get_related_attack_patterns_by_attack_pattern_id(attack_pattern_stix_id)
attack_set = AttackPatternsContainer().get_related_attack_patterns_by_attack_pattern_id(attack_pattern_stix_id)

print("\n* Related attacks: ")
print("By Campaigns", len(attack_set_by_campaign))
print("By ToolMalware", len(attack_set_by_tool))
print("By Asset", len(attack_set_by_asset))
print("--> By All", len(attack_set))

print("\nSearch AttackToCVE by cve id:")

                                                                                                        # CVE-2020-3460
for key, value in AttackToCVEContainer().get_attack_pattern_by_cve_id('CVE-2024-30334').items():
    print("-", key)
    print([at_name.name for at_name in value])

print("\nSearch cve id by attack pattern mitre id:")
for dict_at in AttackToCVEContainer().get_cve_id_by_attack_pattern_mitre_id(
        AttackPatternsContainer().get_object_from_data_by_name('Malicious File')[0].x_mitre_id):
    for key, value in dict_at.items():
        print(key)
        print(value)

print("\n\nPhase and Domain of attack-pattern searched: ",
      AttackPatternsContainer().get_object_from_data_by_id(attack_pattern_stix_id).kill_chain_phases,
      AttackPatternsContainer().get_object_from_data_by_id(attack_pattern_stix_id).x_mitre_domains)

i = 0

print("\n* Probably happened attacks dict for phase: ")
dict_probably_happened = AttackPatternsContainer().get_probably_happened_attack_patterns_grouped_by_phase(
    AttackPatternsContainer().get_object_from_data_by_id(attack_pattern_stix_id))
for key in dict_probably_happened:
    print("  ", key, len(dict_probably_happened[key]))
    enterprise = []
    mobile = []
    ics = []
    atlas = []
    for at_rel_key in dict_probably_happened[key]:
        if 'enterprise-attack' in at_rel_key.x_mitre_domains:
            enterprise.append(i)
        elif 'ics-attack' in at_rel_key.x_mitre_domains:
            ics.append(i)
        elif 'mobile-attack' in at_rel_key.x_mitre_domains:
            mobile.append(i)
        elif 'atlas' in at_rel_key.x_mitre_domains:
            atlas.append(i)
        i += 1

    print("   e", len(enterprise), "  m", len(mobile), "  i", len(ics), "  a", len(atlas), "\n")

print("\n* Probably futured attacks dict for phase: ")
dict_futured = AttackPatternsContainer().get_futured_attack_patterns_grouped_by_phase(
    AttackPatternsContainer().get_object_from_data_by_id(attack_pattern_stix_id))
for key in dict_futured:
    print("  ", key, len(dict_futured[key]))
    enterprise = []
    mobile = []
    ics = []
    atlas = []
    for at_rel_key in dict_futured[key]:
        if 'enterprise-attack' in at_rel_key.x_mitre_domains:
            enterprise.append(i)
        elif 'ics-attack' in at_rel_key.x_mitre_domains:
            ics.append(i)
        elif 'mobile-attack' in at_rel_key.x_mitre_domains:
            mobile.append(i)
        elif 'atlas' in at_rel_key.x_mitre_domains:
            atlas.append(i)
        i += 1

    print("   e", len(enterprise), "  m", len(mobile), "  i", len(ics), "  a", len(atlas), "\n")
