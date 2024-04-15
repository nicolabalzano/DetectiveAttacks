from src.model.container.AttackToCVEContainer import AttackToCVEContainer
from src.model.container.mySTIXContainer.AssetContainer import AssetContainer
from src.model.container.mySTIXContainer.AttackPatternsContainer import AttackPatternsContainer
from src.model.container.mySTIXContainer.CampaignsContainer import CampaignsContainer
from src.model.container.mySTIXContainer.ToolsMalwareContainer import ToolsMalwareContainer
from src.model.interfaceToMitre.conversionType.AttackToCVERetriever import AttackToCVERetriever
from src.model.interfaceToMitre.conversionType.stixConversionType.AssetsRetriever import AssetRetriever
from src.model.interfaceToMitre.conversionType.stixConversionType.AttackPatternsRetriever import \
    AttackPatternsRetriever
from src.model.interfaceToMitre.conversionType.stixConversionType.CampaignsRetriever import CampaignsRetriever
from src.model.interfaceToMitre.conversionType.stixConversionType.ToolsMalwareRetriever import ToolsMalwareRetriever

# INITIALIZE CONTAINER DATA
AttackPatternsContainer(AttackPatternsRetriever().get_all_objects()).get_data()
CampaignsContainer(CampaignsRetriever().get_all_objects()).get_data()
ToolsMalwareContainer(ToolsMalwareRetriever().get_all_objects()).get_data()
AssetContainer(AssetRetriever().get_all_objects()).get_data()
AttackToCVEContainer(AttackToCVERetriever().get_all_objects()).get_data()
