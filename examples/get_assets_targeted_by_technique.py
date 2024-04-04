from pprint import pprint

from mitreattack.stix20 import MitreAttackData


def main():
    mitre_attack_data = MitreAttackData("ics-attack.json")

    # get assets targeted by T0806
    technique_stix_id = "attack-pattern--ead7bd34-186e-4c79-9a4d-b65bcce6ed9d"
    assets_targeted = mitre_attack_data.get_assets_targeted_by_technique(technique_stix_id)

    print(f"Assets targeted by {technique_stix_id} ({len(assets_targeted)}):")
    for a in assets_targeted:
        asset = a["object"]
        print(f"* {asset.name} ({mitre_attack_data.get_attack_id(asset.id)})")
    pprint(assets_targeted[0])

if __name__ == "__main__":
    main()
