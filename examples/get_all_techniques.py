from pprint import pprint

from mitreattack.stix20 import MitreAttackData


def main():
    mitre_attack_data = MitreAttackData("enterprise-attack.json")

    techniques = mitre_attack_data.get_techniques(remove_revoked_deprecated=True)

    print(f"Retrieved {len(techniques)} ATT&CK techniques.")
    pprint(techniques[0].kill_chain_phases)

if __name__ == "__main__":
    main()
