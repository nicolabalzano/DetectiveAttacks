import Threat from "../../../components/threat_show/Threat.jsx";
import {fetchDataAssetAPI} from "../../../components/api/fetchAPI.jsx";

const Asset = () => {

    const primaryInfo = ['Name', 'Type', 'Description'];
    const infoForCardView = ['ID','Aliases', 'Platforms', 'Sectors', 'Domains', 'Revoked']
    const otherImportantInfo = ['Related Assets' ,'Related Attack Patterns'];

    return (
        <Threat primaryInfo={primaryInfo} infoForCardView={infoForCardView} otherImportantInfo={otherImportantInfo} fetchDataFunction={fetchDataAssetAPI}/>
    )

}

export default Asset;