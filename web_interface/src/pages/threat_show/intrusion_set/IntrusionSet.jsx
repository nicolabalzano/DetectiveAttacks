import Threat from "../../../components/threat_show/Threat.jsx";
import {fetchDataIntrusionSetAPI} from "../../../components/api/fetchAPI.jsx";

const Malware = () => {

    const primaryInfo = ['Name', 'Type', 'Description'];
    const infoForCardView = ['ID','Aliases', 'Domains', 'Revoked']
    const otherImportantInfo = ['Related Attack Patterns', 'Tools and Malware used by group', 'Campaigns attributed to group'];

    return (
        <Threat primaryInfo={primaryInfo} infoForCardView={infoForCardView} otherImportantInfo={otherImportantInfo} fetchDataFunction={fetchDataIntrusionSetAPI}/>
    )

}

export default Malware;