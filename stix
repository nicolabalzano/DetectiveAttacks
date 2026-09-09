import sys
from src.dataProvider.container import AttackPatternsContainer

def check_phases():
    ats = AttackPatternsContainer().get_tuple_data()
    stealth_domains = set()
    defense_impairment_domains = set()
    
    for at in ats:
        if not hasattr(at, 'kill_chain_phases'): continue
        domains = getattr(at, 'x_mitre_domains', [])
        
        for phase in at.kill_chain_phases:
            name = phase.phase_name.lower()
            if name == 'stealth':
                stealth_domains.update(domains)
            elif name == 'defense-impairment':
                defense_impairment_domains.update(domains)

    print("STEALTH domini:", stealth_domains)
    print("DEFENSE-IMPAIRMENT domini:", defense_impairment_domains)

if __name__ == "__main__":
    check_phases()
