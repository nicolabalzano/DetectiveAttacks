import React from 'react';
import RenderMitigations from '../../../components/threat_show/RenderMitigations';
import RenderProcedureExamples from '../../../components/threat_show/RenderProcedureExamples';
import RenderDict from '../../../components/threat_show/RenderDict';
import {useLocation} from "react-router-dom";

function Attack() {
    const location = useLocation();
    console.log("Location:", location)
    console.log("Location state:", location.state);
    const searchedResult = location.state ? location.state.searchedResult : null;
    console.log("Searched result:", searchedResult);

    return (
        <div className="container-fluid px-lg-5 margin-top-100">
            <div className="text-primary display-3">
                {searchedResult.Name}
                <p className="text-secondary fs-4 mt-3">{searchedResult.Type}</p>
            </div>
            <div className="mb-4">
                <p className="fs-5">{searchedResult.Description}</p>
                {searchedResult['Detection suggestions'] && (
                    <div>
                        <p className="text-primary display-6 fs-3">Detection suggestions</p>
                        <div>{searchedResult['Detection suggestions']}</div>
                    </div>
                )}
                {searchedResult.Mitigations && (
                    <RenderMitigations mitigations={searchedResult.Mitigations} />
                )}
                {searchedResult['Procedure examples'] && (
                    <RenderProcedureExamples procedureExamples={searchedResult['Procedure examples']} />
                )}
            </div>
        </div>
    );
}

export default Attack;
