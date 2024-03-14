from mitreattack.stix20 import MitreAttackData


class MyMitreAttackData:

    def __init__(self, path_json_mitre_attack: str):
        self.mitre_attack_data = MitreAttackData(path_json_mitre_attack)

    '''
    GET THE TACTIS LIST BY TECHNIQUE NAME
    '''
    def get_tactics_by_technique_name(self, attack_name: str) -> list:
        # get object by name
        techniques = self.mitre_attack_data.get_objects_by_name(attack_name, "attack-pattern")

        # get tactics by (id of) object

        # se la lista non è vuota
        if techniques:
            tactics = self.mitre_attack_data.get_tactics_by_technique((techniques[0])["id"])
            return tactics

        return []

    '''GET TECHNIQUES LIST BY TACTIC NAME'''
    def get_techniques_by_tactic(self, tactic_name: str):
        tactics = self.mitre_attack_data.get_tactics()
        tactics_names = [t["name"] for t in tactics]
        if tactic_name not in tactics_names:
            return []

        techniques = self.mitre_attack_data.get_techniques_by_tactic(
            tactic_name.lower(), "enterprise-attack", remove_revoked_deprecated=True
        )

        return techniques


def main():
    mitre_attack_data = MyMitreAttackData("enterprise-attack.json")

    tactics = mitre_attack_data.get_tactics_by_technique_name("Drive-by Compromise")

    if len(tactics) == 0:
        print("Techniques attacks doesn't exists")
    else:
        for t in tactics:
            print(f"* {t.name}")

    techniques = mitre_attack_data.get_techniques_by_tactic("gg")

    if len(techniques) == 0:
        print("Tactics doesn't exists")
    else:
        print(len(techniques))


if __name__ == "__main__":
    main()
