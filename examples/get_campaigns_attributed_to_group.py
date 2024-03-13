from mitreattack.stix20 import MitreAttackData


def main():
    mitre_attack_data = MitreAttackData("enterprise-attack.json")

    # get campaigns related to G0134
    group_stix_id = "intrusion-set--e44e0985-bc65-4a8f-b578-211c858128e3"
    campaigns_attributed_to_g0134 = mitre_attack_data.get_campaigns_attributed_to_group(group_stix_id)

    print(f"Campaigns attributed to G0134 ({len(campaigns_attributed_to_g0134)}):")
    for c in campaigns_attributed_to_g0134:
        campaign = c["object"]
        print(f"* {campaign.name} ({mitre_attack_data.get_attack_id(campaign.id)})")


if __name__ == "__main__":
    main()
