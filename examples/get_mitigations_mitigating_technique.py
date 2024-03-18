from mitreattack.stix20 import MitreAttackData


def main():
    mitre_attack_data = MitreAttackData("enterprise-attack.json")

    # get groups related to T1014
    technique_stix_id = "attack-pattern--57340c81-c025-4189-8fa0-fc7ede51bae4"
    mitigations_mitigating = mitre_attack_data.get_mitigations_mitigating_technique(technique_stix_id)
    print(type(mitigations_mitigating))

    print(f"Mitigations mitigating ({len(mitigations_mitigating)}):")
    for m in mitigations_mitigating:
        mitigation = m["object"]
        print(f"* {mitigation.name} ({mitre_attack_data.get_attack_id(mitigation.id)})")
        # print(type(mitigation))
        # print(mitigation)

if __name__ == "__main__":
    main()
