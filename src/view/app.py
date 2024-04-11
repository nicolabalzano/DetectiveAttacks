from flask import Flask, render_template

from src.domain.container.AttackToCVEContainer import AttackToCVEContainer
from src.domain.container.mySTIXContainer.AssetContainer import AssetContainer
from src.domain.container.mySTIXContainer.AttackPatternsContainer import AttackPatternsContainer
from src.domain.container.mySTIXContainer.CampaignsContainer import CampaignsContainer
from src.domain.container.mySTIXContainer.ToolsMalwareContainer import ToolsMalwareContainer
from src.domain.interfaceToMitre.conversionType.AttackToCVERetriever import AttackToCVERetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.AssetsRetriever import AssetRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.AttackPatternsRetriever import \
    AttackPatternsRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.CampaignsRetriever import CampaignsRetriever
from src.domain.interfaceToMitre.conversionType.stixConversionType.ToolsMalwareRetriever import ToolsMalwareRetriever
from src.domain.interfaceToMitre.mitreData.FetchData import fetch_enterprise_data, fetch_mobile_data, fetch_ics_data, \
    fetch_atlas_data, fetch_attack_to_cve_data
from src.domain.interfaceToMitre.mitreData.mitreAttackToCVE.AttackBert import AttackBert

app = Flask(__name__)


@app.route('/')
def index():
    fetch_enterprise_data()
    fetch_mobile_data()
    fetch_ics_data()
    fetch_atlas_data()
    fetch_attack_to_cve_data()

    # init language semantic model
    AttackBert()

    # attack_pattern_stix_id = "attack-pattern--57340c81-c025-4189-8fa0-fc7ede51bae4"
    # attack_pattern_name = "Drive-by Compromise"
    campaign_stix_id = "campaign--b4e5a4a9-f3be-4631-ba8f-da6ebb067fac"
    tool_malware_stix_id = "tool--b76b2d94-60e4-4107-a903-4a3a7622fb3b"

    # container
    l1 = len(AttackPatternsContainer(AttackPatternsRetriever().get_all_objects()).get_data())
    print("\ndimension AttackPatternsContainer", l1)
    l2 = len(CampaignsContainer(CampaignsRetriever().get_all_objects()).get_data())
    print("dimension CampaignsContainer", l2)
    l3 = len(ToolsMalwareContainer(ToolsMalwareRetriever().get_all_objects()).get_data())
    print("dimension ToolsMalwareContainer", l3)
    l4 = len(AssetContainer(AssetRetriever().get_all_objects()).get_data())
    print("dimension AssetContainer", l4)
    l5 = len(AttackToCVEContainer(AttackToCVERetriever().get_all_objects()).get_data())
    print("dimension AttackToCVEContainer", l5)

    lenghts = [l1, l2, l3, l4, l5]
    return render_template('index.html', lenghts_of_container=lenghts)


if __name__ == '__main__':
    app.run(debug=True)
