import React, {useEffect, useState} from 'react';
import RenderMitigations from '../../../components/threat_show/RenderMitigations';
import RenderProcedureExamples from '../../../components/threat_show/RenderProcedureExamples';
import RenderDict from '../../../components/threat_show/RenderDict';
import {useLocation} from "react-router-dom";
import {fetchDataAttackAPI} from "../../../components/api/fetchAPI.jsx";
import ImportantInfo from "../../../components/threat_show/ImportantInfo.jsx";
import OtherImportantInfo from "../../../components/threat_show/OtherImoprtantInfo.jsx";



const Attack = () => {
    const [searchedResult, setSearchedResult] = useState(null);
    const location = useLocation();
    const otherImportantInfo = ['Detection suggestions', 'Mitigations', 'Procedure examples'];
    const [otherImportantInfoDict, setOtherImportantInfo] = useState(null);

    useEffect(() => {
        const idObj = location.state.id;

        // FETCH DATA FROM API
        fetchDataAttackAPI(idObj).then((r) => {
            setSearchedResult(r.data);
        });
    } , []);

    // SET OTHER IMPORTANT INFO DICT
    useEffect(() => {
        if (searchedResult) {
            var newDict = {};
            for (let key of otherImportantInfo) {
                if (searchedResult.hasOwnProperty(key)) {
                    newDict[key] = searchedResult[key];
                    // console.log(otherImportantInfoDict);
                }
            }
            setOtherImportantInfo(newDict)
        }
    }, [searchedResult]);

    return (
        <div className="container-fluid px-lg-5 margin-top-100">
            {searchedResult && otherImportantInfoDict && (
                <>
                    <ImportantInfo importantInfoDict={searchedResult}/>
                    <OtherImportantInfo otherImportantInfoDict={otherImportantInfoDict}/>
                </>
            )}
        </div>
    );
}

export default Attack;
