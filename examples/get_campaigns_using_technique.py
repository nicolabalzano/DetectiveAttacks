from mitreattack.stix20 import MitreAttackData


def main():
    mitre_attack_data = MitreAttackData("enterprise-attack.json")

    # get campaigns related to T1049
    technique_stix_id = "attack-pattern--57340c81-c025-4189-8fa0-fc7ede51bae4"
    campaigns_using_t1049 = mitre_attack_data.get_campaigns_using_technique(technique_stix_id)

    print(f"Campaigns using T1049 ({len(campaigns_using_t1049)}):")
    for c in campaigns_using_t1049:
        campaign = c["object"]
        print(f"* {campaign.name} ({mitre_attack_data.get_attack_id(campaign.id)})")


if __name__ == "__main__":
    main()
