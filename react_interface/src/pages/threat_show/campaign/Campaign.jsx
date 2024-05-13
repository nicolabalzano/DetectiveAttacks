import Threat from "../../../components/threat_show/Threat.jsx";
import {fetchDataCampaignAPI} from "../../../components/api/fetchAPI.jsx";

const Campaign = () => {

    const primaryInfo = ['Name', 'Type', 'Description'];
    const infoForCardView = ['ID','Aliases', 'Domains', 'Revoked']
    const otherImportantInfo = ['Related Attack Patterns'];

    return (
        <Threat primaryInfo={primaryInfo} infoForCardView={infoForCardView} otherImportantInfo={otherImportantInfo} fetchDataFunction={fetchDataCampaignAPI}/>
    )

}

export default Campaign;