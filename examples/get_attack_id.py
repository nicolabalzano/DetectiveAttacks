from mitreattack.stix20 import MitreAttackData


def main():
    mitre_attack_data = MitreAttackData("enterprise-attack.json")

    attack_id = mitre_attack_data.get_attack_id("attack-pattern--57340c81-c025-4189-8fa0-fc7ede51bae4")

    print(attack_id)


if __name__ == "__main__":
    main()
