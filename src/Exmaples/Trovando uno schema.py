from mitreattack.stix20 import MitreAttackData


def print_techniques(techniques: list) -> set:
    set_techniques = set()
    for t in techniques:
        set_techniques.add(t["object"].name)
        #print(f"\n    *{t["object"].name}")
    #print(type(set_techniques_name))
    return set_techniques

mitre_attack_data = MitreAttackData("enterprise-attack.json")

# get campaigns related to T1049
technique_stix_id = "attack-pattern--7e150503-88e7-4861-866b-ff1ac82c4475"
set_techniques_name = set()

campaigns_using_t1049 = mitre_attack_data.get_campaigns_using_technique(technique_stix_id)
print(f"Campaigns using T1049 ({len(campaigns_using_t1049)}):")
for c in campaigns_using_t1049:
    campaign = c["object"]
    print(f"* {campaign.name} ({mitre_attack_data.get_attack_id(campaign.id)})")
    set_techniques_name.update(print_techniques(mitre_attack_data.get_techniques_used_by_campaign(campaign.id)))

group_using_t1049 = mitre_attack_data.get_groups_using_technique(technique_stix_id)
print(f"\n {len(set_techniques_name)} TECHNIQUES IDENTIFY:")


print(f"\nGroup using T1049 ({len(group_using_t1049)}):")
for c in group_using_t1049:
    group = c["object"]
    print(f"* {group.name} ({mitre_attack_data.get_attack_id(group.id)})")
    set_techniques_name.update(print_techniques(mitre_attack_data.get_techniques_used_by_group(group.id)))
print(f"\n {len(set_techniques_name)} TECHNIQUES IDENTIFY:")


software_using_t1049 = mitre_attack_data.get_software_using_technique(technique_stix_id)

print(f"\nSoftware using T1049 ({len(group_using_t1049)}):")
for c in software_using_t1049:
    software = c["object"]
    print(f"* {software.name} ({mitre_attack_data.get_attack_id(software.id)})")
    set_techniques_name.update(print_techniques(mitre_attack_data.get_techniques_used_by_software(software.id)))
print(f"\n {len(set_techniques_name)} TECHNIQUES IDENTIFY:")

# dividerle tra le tattiche e capire quelle future o precedenti

'''
for t in set_techniques_name:
    print(f"\n    {t}")
'''