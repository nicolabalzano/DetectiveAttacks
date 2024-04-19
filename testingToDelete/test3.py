from src.model.container import AttackPatternsContainer
from src.model.container.mySTIXContainer.ToolsMalwareContainer import ToolsMalwareContainer

for tm in ToolsMalwareContainer().get_object_using_attack_pattern_by_attack_pattern_id(AttackPatternsContainer().get_object_from_data_by_mitre_id('T1456').id):
    print(tm.name)
    for at, rel in tm.attack_patterns_and_relationships.items():
        print("   ", at.name)
        print("   ", rel.relationship_type)
        print("   ", rel.description)

