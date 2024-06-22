import Threat from "../../../components/threat_show/Threat.jsx";
import {fetchDataAttackAPI} from "../../../components/api/fetchAPI.jsx";

const Attack = () => {

    const primaryInfo = ['Name', 'Type', 'Description'];
    const infoForCardView = ['ID', 'Domains', 'Mitre Kill Chain phases', 'Kill Chain phases', 'Platforms', 'Deprecated']
    const otherImportantInfo = ['Detection suggestions', 'Mitigations', 'Procedure examples', 'Campaigns that exploit this attack pattern', 'Targeted assets',
        'ATT&CK and ATLAS techniques that can lead to this', 'ATT&CK and ATLAS techniques that can occur after this', 'All ATT&CK and ATLAS techniques that can encounter'];

    return (
        <Threat primaryInfo={primaryInfo} infoForCardView={infoForCardView} otherImportantInfo={otherImportantInfo} fetchDataFunction={fetchDataAttackAPI}/>
    )

}

export default Attack;