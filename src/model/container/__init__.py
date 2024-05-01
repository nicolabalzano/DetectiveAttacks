from src.model.container.vulnerabilityContainer.MitreToCVEContainer import MitreToCVEContainer
from src.model.container.mySTIXContainer.AssetContainer import AssetContainer
from src.model.container.mySTIXContainer.AttackPatternsContainer import AttackPatternsContainer
from src.model.container.mySTIXContainer.CampaignsContainer import CampaignsContainer
from src.model.container.mySTIXContainer.ToolsMalwareContainer import ToolsMalwareContainer
from src.model.container.vulnerabilityContainer.MitreToCWEContainer import MitreToCWEContainer
from src.model.interfaceToMitre.conversionType.attackToVulnerabilityRetriever.MitreToCVERetriever import MitreToCVERetriever
from src.model.interfaceToMitre.conversionType.attackToVulnerabilityRetriever.MitreToCWERetriever import \
    MitreToCWERetriever
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
MitreToCVEContainer(MitreToCVERetriever().get_all_objects()).get_data()
MitreToCWEContainer(MitreToCWERetriever().get_all_objects()).get_data()

