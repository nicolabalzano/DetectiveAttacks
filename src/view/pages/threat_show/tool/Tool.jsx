import Threat from "../../../components/threat_show/Threat.jsx";
import {fetchDataToolAPI} from "../../../components/api/fetchAPI.jsx";

const Tool = () => {

    const primaryInfo = ['Name', 'ID', 'Type', 'Description'];
    const infoForCardView = ['ID','Aliases', 'Domains', 'Platforms', 'Revoked']
    const otherImportantInfo = ['Related Attack Patterns'];

    return (
        <Threat primaryInfo={primaryInfo} infoForCardView={infoForCardView} otherImportantInfo={otherImportantInfo} fetchDataFunction={fetchDataToolAPI}/>
    )

}

export default Tool;