import TableView from "../../components/threat_show/util/TableView.jsx";
import {
    fetchDataAttackPatternsGroupedByPhaseAPI,
    fetchDataDomains, fetchDataReportGroupsAPI,
    fetchDataPlatforms, fetchDataCKCPhases
} from "../../components/api/fetchAPI.jsx";
import React, { useEffect, useState } from "react";
import SearchBar from "../../components/search_bar/SearchBar.jsx";
import { Skeleton } from "@mui/material";
import('../../scss/util.scss')

const TableAttackPatternsGroupedByPhases = () => {

    // store of the attack patterns grouped by cyber kill chain phases
    const [atGroupedByPhase, setAtGroupedByPhase] = useState([])
    // store of the attack patterns in view (updated by search)
    const [atGroupByPhaseInView, setAtGroupByPhaseInView] = useState([]);
    // store of the attack patterns selected by the user
    const [selectedAt, setSelectedAt] = useState([])
    // store of the filter of selected domains of attack patterns
    const [listOfFilterDomains, setListOfFilterDomains] = useState([]);
    const [selectedDomains, setSelectedDomains] = useState([]);
    // store of the filter of selected platforms of attack patterns
    const [listOfFilterPlatforms, setListOfFilterPlatforms] = useState([]);
    const [selectedPlatforms, setSelectedPlatforms] = useState([]);
    // store of the search term
    const [searchTerm, setSearchTerm] = useState("");
    // loading
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        document.title = "Attack Patterns grouped by Cyber Kill Chain Phases";
        setLoading(true);

        Promise.all([
            fetchDataAttackPatternsGroupedByPhaseAPI(),
            fetchDataPlatforms(),
            fetchDataDomains(),
            fetchDataCKCPhases()
        ]).then(([attackPatternsResponse, platformsResponse, domainsResponse, ckcPhasesResponse]) => {
            const cyberKillChainPhases = ckcPhasesResponse.data;
            const atsOrdered = Object.fromEntries(
                cyberKillChainPhases
                    .filter(phase => phase in attackPatternsResponse.data)
                    .map(phase => [phase, attackPatternsResponse.data[phase]])
                )
            setAtGroupedByPhase(atsOrdered);
            setAtGroupByPhaseInView(atsOrdered);
            setListOfFilterPlatforms(platformsResponse.data.sort());
            setSelectedPlatforms(platformsResponse.data.sort());
            setListOfFilterDomains(domainsResponse.data);
            setSelectedDomains(domainsResponse.data);
            setLoading(false);
        }).catch((e) => {
            console.error(e);
        });
    }, []);

    // function checkIfIsSelected(types, selectedObj) {
    //     selectedObj.some(obj =>
    //         types.some(type =>
    //             type.toLowerCase() === obj.toLowerCase() ||
    //             type.toLowerCase().includes(obj.toLowerCase()))
    //     )
    // }

    useEffect(() => {
        let filteredAtGroupedByPhase = {};

        if (Object.keys(atGroupedByPhase).length > 0) {
            const filteredAtGroupedByPhase = Object.entries(atGroupedByPhase).reduce((acc, [phase, ats]) => {
                const filteredAts = ats.filter(at =>
                    selectedDomains.some(selectedDomain =>
                        at.Domains.toLowerCase().includes(selectedDomain.toLowerCase())
                    ) &&
                    selectedPlatforms.some(platform =>
                        at.Platforms.toLowerCase().includes(platform.toLowerCase())
                    ) &&
                    (
                        (at.Name && at.Name.toLowerCase().includes(searchTerm.toLowerCase())) ||
                        (at.ID && at.ID.toLowerCase().includes(searchTerm.toLowerCase()))
                    )
                );
    
                if (filteredAts.length > 0) {
                    acc[phase] = filteredAts;
                }
    
                return acc;
            }, {});
    
            setAtGroupByPhaseInView(filteredAtGroupedByPhase);
        }
    }, [selectedDomains, selectedPlatforms, searchTerm, atGroupedByPhase]);

    function CheckboxComponent({ list_of_filter, setSelected, selected }) {

        const handleCheckboxChange = (event, setSelected, selected) => {
            const { checked, id } = event.target;
            if (checked) {
                setSelected((prevSelected) => [...prevSelected, id]);
            } else {
                setSelected((prevSelected) => prevSelected.filter((type) => type !== id));
            }
        };

        return (
            <div className="">
                {list_of_filter.map((type) => (
                    <div className="text-secondary me-4 d-inline-block" key={type}>
                        <input
                            className="form-check-input checkbox-type me-2"
                            type="checkbox"
                            id={type}
                            onChange={(event => handleCheckboxChange(event, setSelected, selected))}
                            checked={selected.includes(type)}
                        />
                        <label className="form-check-label" htmlFor={type}>
                            {type}
                        </label>
                    </div>
                ))}
            </div>
        );
    }

    function handleSearch(searchTerm) {
        setSearchTerm(searchTerm)
    }

    return (
        <div className="margin-top-100 mx-5 d-flex justify-content-center align-items-center">
            <div className="">
                <h1 className="text-center h1 mb-5">Attack Patterns grouped by Cyber Kill Chain Phases</h1>
                <SearchBar onSearch={handleSearch} />
                <div className="row d-flex mb-3 px-5 ">
                    {/* Filter of platforms */}
                    <div className="row text-secondary ">
                        <span className="fw-semibold">Filter by platforms</span>
                        {loading
                            ?
                            <div className="d-flex justify-content-center w-auto mt-3">
                                <Skeleton variant="rounded" animation="wave" width={1100} height={80} /></div>
                            :
                            <div className="ms-3 fs-6">
                                <CheckboxComponent list_of_filter={listOfFilterPlatforms} setSelected={setSelectedPlatforms}
                                    selected={selectedPlatforms} />
                            </div>
                        }

                    </div>
                    {/* Filter of domains */}
                    <div className="row mt-3 text-secondary">
                        <span className="fw-semibold">Filter by domains</span>
                        {loading
                            ?
                            <div className="d-flex justify-content-center w-auto mt-3">
                                <Skeleton variant="rounded" animation="wave" width={1100} height={50} /></div>
                            :
                            <div className="ms-3 fs-6">
                                <CheckboxComponent list_of_filter={listOfFilterDomains} setSelected={setSelectedDomains}
                                    selected={selectedDomains} />
                            </div>

                        }
                    </div>

                </div>
                {
                    loading ?
                        <div className="d-flex justify-content-center w-auto mt-5"><Skeleton variant="rounded"
                            animation="wave"
                            width={1100} height={1000} />
                        </div>
                        :
                        <div>

                            {/* Button to generate the report */}
                            <button className="position-fixed bottom-0 end-0 me-3 mb-3 btn btn-primary px-3 shadow reduce-font"
                                onClick={() => {
                                    let selectedAtFormatted = [];
                                    // const T = /T\d+/;
                                    // const AML = /AML.T\d+/;
                                    // Reformat the id to take only the id
                                    console.log(selectedAt)
                                    selectedAt.forEach((at) => {
                                        // const atFormatted = at.replace(/_/g, '.')
  
                                        // const matchT = atFormatted.match(T);
                                        // const matchAML = atFormatted.match(AML);

                                        // if (matchAML) {
                                        //     const indexOfAML = atFormatted.indexOf(matchAML[0]);
                                        //     console.log(atFormatted.substring(indexOfAML).replace(/\.0$/, ''))
                                        //     selectedAtFormatted.push(atFormatted.substring(indexOfAML).replace(/\.0$/, ''));
                                        // }
                                        // else if (matchT) {
                                        //     const indexOfT = atFormatted.indexOf(matchT[0]);
                                        //     console.log(atFormatted.substring(indexOfT).replace(/\.0$/, ''))
                                        //     selectedAtFormatted.push(atFormatted.substring(indexOfT).replace(/\.0$/, ''));
                                        // }
                                        const indexToSplit = at.indexOf("__");
                                        const atFormatted = at.substring(indexToSplit + 2).replace(/_/g, '.').replace(/\.0$/, '');
                                        selectedAtFormatted.push(atFormatted);
                                        console.log(atFormatted)
                                    });
                                    fetchDataReportGroupsAPI(selectedAtFormatted).catch((e) => {
                                        alert("An error occurred while generating the report. Please try again later or check console for more info.");
                                        console.error(e);
                                    });
                                }}
                            >Generate the report</button>

                            {/* Big table */}
                            <TableView infoDict={atGroupByPhaseInView} selectedAt={selectedAt}
                                setSelectedAt={setSelectedAt} />
                        </div>
                }
            </div>
        </div>
    );

}

export default TableAttackPatternsGroupedByPhases;