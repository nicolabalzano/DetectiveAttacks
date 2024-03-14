from mitreattack.stix20 import MitreAttackData


def get_tactics_by_technique_name(attack_name: str):
    mitre_attack_data = MitreAttackData("enterprise-attack.json")

    # get object by name
    techniques = mitre_attack_data.get_objects_by_name(attack_name, "attack-pattern")

    # get tactics by (id of) object

    # se la lista non è vuota
    if techniques:
        tactics = mitre_attack_data.get_tactics_by_technique((techniques[0])["id"])
        return tactics

    return None


def main():
    tactics = get_tactics_by_technique_name("Drive-by Compromise")

    if tactics is None:
        print("Techniques attacks doesn't exists")
    else:
        print(f"Retrieved {len(tactics)} tactic(s):")
        for t in tactics:
            print(f"* {t.name}")


if __name__ == "__main__":
    main()
