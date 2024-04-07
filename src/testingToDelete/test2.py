from src.domain.container.mySTIXContainer.AttackPatternsContainer import AttackPatternsContainer
from src.domain.container.AttackToCVEContainer import AttackToCVEContainer
from src.domain.interfaceToMitre.conversionType.stixConversionType.AttackPatternsRetriever import AttackPatternsRetriever
from src.domain.interfaceToMitre.conversionType.AttackToCVERetriever import AttackToCVERetriever
from src.domain.interfaceToMitre.mitreData.FetchData import fetch_attack_to_cve_data

"""
pprint(list(mitre_atlas_data.get_all_techniques_used_by_all_case_studies().values())[0])
pprint(len(mitre_atlas_data.get_case_studies()))
pprint(len(mitre_atlas_data.get_all_techniques_used_by_all_case_studies()))
"""

"""
AttackPatternsContainer(AttackPatternsRetriever().get_all_objects())

cs = CampaignsContainer(CampaignsRetriever().get_all_objects()).get_object_from_data_by_name('Control Access to ML Models and Data in Production')[0]

pprint(cs)

for at in MITRE_ATLAS_DATA.get_techniques_used_by_mitigation(cs.id):
    pprint(at['object'].name)
"""

fetch_attack_to_cve_data()

print(AttackPatternsContainer(AttackPatternsRetriever().get_all_objects()).get_data()[0].name)
print(AttackPatternsContainer().get_object_from_data_by_mitre_id('T1055.011').name)
for a_to_cve in AttackToCVEContainer(AttackToCVERetriever().get_all_objects()).get_data():
    print(a_to_cve["CVE ID"],
          [AttackPatternsContainer().get_object_from_data_by_mitre_id(a).name if AttackPatternsContainer().get_object_from_data_by_mitre_id(a) else a for a in
           a_to_cve["Primary Impact"]],
          [AttackPatternsContainer().get_object_from_data_by_mitre_id(a).name if AttackPatternsContainer().get_object_from_data_by_mitre_id(a) else a for a in
           a_to_cve["Secondary Impact"]],
          [AttackPatternsContainer().get_object_from_data_by_mitre_id(a).name if AttackPatternsContainer().get_object_from_data_by_mitre_id(a) else a for a in
           a_to_cve["Exploitation Technique"]],
          [AttackPatternsContainer().get_object_from_data_by_mitre_id(a).name if AttackPatternsContainer().get_object_from_data_by_mitre_id(a) else a for a in
           a_to_cve["Uncategorized"]]
          )

print(AttackPatternsContainer().get_data()[0].courses_of_action_and_relationship)
print(AttackPatternsContainer().get_object_from_data_by_name('Default Credentials')[0].x_mitre_id)

print("\nSearch AttackToCVE by cve id:")
for at in AttackToCVEContainer().get_attack_pattern_by_cve_id('CVE-2019-15243')["Primary Impact"]:
    print(AttackPatternsContainer().get_object_from_data_by_mitre_id(at).x_mitre_id)
for at in AttackToCVEContainer().get_attack_pattern_by_cve_id('CVE-2019-15243')["Secondary Impact"]:
    print(AttackPatternsContainer().get_object_from_data_by_mitre_id(at).x_mitre_id)
for at in AttackToCVEContainer().get_attack_pattern_by_cve_id('CVE-2019-15243')["Exploitation Technique"]:
    print(AttackPatternsContainer().get_object_from_data_by_mitre_id(at).x_mitre_id)
for at in AttackToCVEContainer().get_attack_pattern_by_cve_id('CVE-2019-15243')["Uncategorized"]:
    print(AttackPatternsContainer().get_object_from_data_by_mitre_id(at).x_mitre_id)

# print(MITRE_ATLAS_DATA.get_techniques()[0])
# print(MITRE_ATLAS_DATA.get_all_mitigations_mitigating_all_techniques())
# print(MITRE_ATLAS_DATA.get_mitigations_mitigating_technique("attack-pattern--f32a49d9-63d6-4c33-9256-81279fd0bec9"))
