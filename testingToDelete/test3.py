from pprint import pprint

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

for obj in [obj for obj in CampaignsContainer().get_data() if obj.x_mitre_domains == ['atlas']]:
    if obj.x_mitre_id == '':
        print("id", obj.x_mitre_id, "name=", obj.name)

obj = [obj for obj in CampaignsContainer().get_data() if obj.x_mitre_domains == ['atlas']][20]
pprint(obj.external_references)

for obj in CampaignsRetriever().get_all_objects():
