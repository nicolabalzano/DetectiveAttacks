from mitreattack.stix20 import MitreAttackData


def main():
    mitre_attack_data = MitreAttackData("mobile-attack.json")

    # get techniques used by S0349
    # software_stix_id = "tool--b76b2d94-60e4-4107-a903-4a3a7622fb3b"
    software_stix_id = "tool--1622fd3d-fcfc-4d02-ac49-f2d786f79b81"
    techniques_used_by_s0349 = mitre_attack_data.get_techniques_used_by_software(software_stix_id)
    print(f"Techniques used by S0349 ({len(techniques_used_by_s0349)}):")
    for t in techniques_used_by_s0349:
        technique = t["object"]
        print(f"* {technique.name} ({mitre_attack_data.get_attack_id(technique.id)})")

    print(techniques_used_by_s0349)

if __name__ == "__main__":
    main()
