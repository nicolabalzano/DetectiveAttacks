import React, { useEffect, useState } from 'react';
import TableView from "./TableView.jsx";
import SwitchView from "../../switch_view_selector/SwitchView.jsx";
import { useNavigate } from "react-router-dom";
import { isDict, handleDropdown } from "./Utils.jsx";
import HierarchicView from "./HierarchicView.jsx";
import { fetchDataCKCPhases } from "../../api/fetchAPI.jsx";

function OtherImportantInfo({ otherImportantInfoDict }) {
    // store of the attack patterns selected by the user
    const [selectedAt, setSelectedAt] = useState([])
    const navigate = useNavigate();
    const [cyberKillChainPhases, setCyberKillChainPhases] = useState([]);
    
    let tableCounter = 0;


    function reorderDictCKCPhases(infoDict) {
        return (
            Object.fromEntries(
                cyberKillChainPhases
                    .filter(phase => phase in infoDict)
                    .map(phase => [phase, infoDict[phase]])
            )
        );
}


    useEffect(() => {
        fetchDataCKCPhases().then((r) => {
            setCyberKillChainPhases(r.data);
        }).catch((e) => {
            console.error(e);
        });
    }, []);

    return (
        <>
            {Object.entries(otherImportantInfoDict).map(([title, value], index) => (
                <div key={index}>
                    <p className="text-primary display-6 fs-3 mt-4">{title}
                        <span>
                            <i className="bi bi-caret-down-fill fs-5" role="button" id={title} onClick={(e) => handleDropdown(e)}></i>
                        </span>
                    </p>
                    {
                        value && (
                            <div className="d-none" id={title + '_div'}>

                                {
                                    isDict(value)
                                        ? // If it's an array like Related Attack Patterns to show Phases
                                        (
                                            <>
                                                {/* Switch view */}
                                                <SwitchView startId={title} />
                                                <div className="row ms-5 d-none d-flex justify-content-center " id={title + '_table'}>

                                                    {/*Button go to Big table view*/}
                                                    <button className="btn btn-outline-primary px-2 w-100 mt-3 text-uppercase fw-semibold"
                                                        onClick={() => { navigate('/attack_patterns_by_phase', { state: { alreadySelected: selectedAt } }) }}
                                                    >Continue to generate the report</button>

                                                    {/* Table view */}
                                                    <TableView infoDict={reorderDictCKCPhases(value)} selectedAt={selectedAt} setSelectedAt={setSelectedAt} tableCount={++tableCounter} />
                                                </div>
                                            </>
                                        ) : null
                                    //: null
                                }

                                {/*Hierarchic view*/}
                                <div id={title + '_hierarchic'}>
                                    {Array.isArray(value) ?
                                        value.map((subDict, subIndex) => (
                                            <HierarchicView key={subIndex} subDict={subDict} keyForSameIdWords={index} />
                                        ))
                                        // If it's a dict like Related Attack Patterns to show Phases
                                        : isDict(value) ? 
                                            Object.entries(reorderDictCKCPhases(value)).map(([phase, subValue], subIndex) => (
                                                <HierarchicView key={subIndex} subDict={{[phase]: subValue}} keyForSameIdWords={index} />
                                            ))
                                            :
                                            <div>{value}</div>
                                    }
                                </div>
                            </div>
                        )
                    }

                </div>
            ))}
        </>
    );
}

export default OtherImportantInfo;
