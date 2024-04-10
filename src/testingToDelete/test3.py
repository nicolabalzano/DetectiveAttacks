import nvdlib
from allennlp.predictors import Predictor

from src.domain.container.mySTIXContainer.AssetContainer import AssetContainer
from src.domain.container.mySTIXContainer.AttackPatternsContainer import AttackPatternsContainer
from src.domain.container.AttackToCVEContainer import AttackToCVEContainer
from src.domain.container.mySTIXContainer.CampaignsContainer import CampaignsContainer
from src.domain.container.mySTIXContainer.ToolsMalwareContainer import ToolsMalwareContainer
from src.domain.interfaceToMitre.conversionType.AttackToCVERetriever import AttackToCVERetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.AssetsRetriever import AssetRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.AttackPatternsRetriever import \
    AttackPatternsRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.CampaignsRetriever import CampaignsRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.ToolsMalwareRetriever import ToolsMalwareRetriever
from src.domain.interfaceToMitre.mitreData.FetchData import *

fetch_enterprise_data()
fetch_mobile_data()
fetch_ics_data()
fetch_atlas_data()
fetch_attack_to_cve_data()

# container

print("\ndimension AttackPatternsContainer",
      len(AttackPatternsContainer(AttackPatternsRetriever().get_all_objects()).get_data()))
print("dimension CampaignsContainer", len(CampaignsContainer(CampaignsRetriever().get_all_objects()).get_data()))
print("dimension ToolsMalwareContainer",
      len(ToolsMalwareContainer(ToolsMalwareRetriever().get_all_objects()).get_data()))
print("dimension AssetContainer", len(AssetContainer(AssetRetriever().get_all_objects()).get_data()))
print("dimension AttackToCVEContainer", len(AttackToCVEContainer(AttackToCVERetriever().get_all_objects()).get_data()))

r = nvdlib.searchCVE(cveId='CVE-2024-30334')[0]
print(r.descriptions[0].value)
print(r.id, r.id.split('-')[1], r.descriptions[0].value.split('.')[0])

# pprint(r)

# Carica il modello SRL pre-allenato
predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/bert-base-srl-2020.11.19.tar.gz")

# Frase su cui eseguire SRL
sentence = "The quick brown fox jumps over the lazy dog."

# Esegui SRL sulla frase
srl_result = predictor.predict(sentence=sentence)

# Stampa i risultati
for verb in srl_result['verbs']:
    print(f"Verbo: {verb['verb']}")
    for tag, description in verb['description'].items():
        print(f"  {tag}: {description}")
    print("\n")
