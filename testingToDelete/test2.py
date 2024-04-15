import nvdlib
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from wandb.wandb_torch import torch
import transformers

from src.model.container.mySTIXContainer.AssetContainer import AssetContainer
from src.model.container.mySTIXContainer.AttackPatternsContainer import AttackPatternsContainer
from src.model.container.AttackToCVEContainer import AttackToCVEContainer
from src.model.container.mySTIXContainer.CampaignsContainer import CampaignsContainer
from src.model.container.mySTIXContainer.ToolsMalwareContainer import ToolsMalwareContainer
from src.model.interfaceToMitre.conversionType.AttackToCVERetriever import AttackToCVERetriever
from src.model.interfaceToMitre.conversionType.stixConversionType.AssetsRetriever import AssetRetriever
from src.model.interfaceToMitre.conversionType.stixConversionType.AttackPatternsRetriever import \
    AttackPatternsRetriever
from src.model.interfaceToMitre.conversionType.stixConversionType.CampaignsRetriever import CampaignsRetriever
from src.model.interfaceToMitre.conversionType.stixConversionType.ToolsMalwareRetriever import ToolsMalwareRetriever
from src.model.interfaceToMitre.mitreData.FetchData import *
from src.model.interfaceToMitre.mitreData.mitreAttackToCVE.SentenceSimilarityModel import SentenceSimilarityModel

cve = nvdlib.searchCVE(cveId='CVE-2024-3388')[0]
print(cve.descriptions[0].value)

for at in AttackToCVEContainer().get_attack_pattern_by_cve_id('CVE-2024-3388')['uncategorized']:
    print(AttackPatternsContainer().get_object_from_data_by_mitre_id(at.x_mitre_id).name)
    print(AttackPatternsContainer().get_object_from_data_by_mitre_id(at.x_mitre_id).x_mitre_models)
    print(SentenceSimilarityModel().check_similarity(cve.descriptions[0].value, AttackPatternsContainer().get_object_from_data_by_mitre_id(at.x_mitre_id).description))
    print("\n")