import Threat from "../../../components/threat_show/Threat.jsx";
import {fetchDataToolAPI} from "../../../components/api/fetchAPI.jsx";

const Tool = () => {

    const primaryInfo = ['Name', 'Type', 'Description'];
    const infoForCardView = ['ID','Aliases', 'Domains', 'Platforms', 'Revoked']
    const otherImportantInfo = ['Realetd ATT&CK and ATLAS techniques'];

    return (
        <Threat primaryInfo={primaryInfo} infoForCardView={infoForCardView} otherImportantInfo={otherImportantInfo} fetchDataFunction={fetchDataToolAPI}/>
    )

}

export default Tool;