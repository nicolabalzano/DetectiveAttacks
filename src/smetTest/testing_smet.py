from src.domain.container.mySTIXContainer.AttackPatternsContainer import AttackPatternsContainer
from src.domain.interfaceToMitre.conversionType.stixConversionType.AttackPatternsRetriever import \
    AttackPatternsRetriever
from src.domain.interfaceToMitre.mitreData.FetchData import *
from src.smetTest.smet import map_text, predict_techniques, get_AVs

fetch_enterprise_data()
fetch_mobile_data()
fetch_ics_data()
fetch_atlas_data()
fetch_attack_to_cve_data()

print("\ndimension AttackPatternsContainer",
      len(AttackPatternsContainer(AttackPatternsRetriever().get_all_objects()).get_data()))

text = ("While supply chain compromise can impact any component of hardware or software, adversaries looking to gain "
        "execution have often focused on malicious additions to legitimate software in software distribution or update "
        "channels.(Citation: Avast CCleaner3 2018)(Citation: Microsoft Dofoil 2018)(Citation: Command Five SK 2011) "
        "Targeting may be specific to a desired victim set or malicious software may be distributed to a broad set of "
        "consumers but only move on to additional tactics on specific victims.(Citation: Symantec Elderwood Sept "
        "2012)(Citation: Avast CCleaner3 2018)(Citation: Command Five SK 2011) Popular open source projects that are "
        "used as dependencies in many applications may also be targeted as a means to add malicious code to users of "
        "the dependency.(Citation: Trendmicro NPM Compromise)")

# print(predict_techniques(text, 0))
# print(map_text(text))
avs = get_AVs(text)
print(avs)

# Crea un nuovo set che contiene solo gli AVs senza 'Citation'
avs_without_citation = {av for av in avs if 'Citation' not in av}

print(avs_without_citation)
