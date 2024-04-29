import React, {useEffect, useState} from 'react';
import RenderDict from './util/RenderDict';
import {useLocation, useParams} from "react-router-dom";
import {fetchDataAttackAPI} from "../api/fetchAPI.jsx";
import ImportantInfo from "./util/ImportantInfo.jsx";
import OtherImportantInfo from "./util/OtherImportantInfo.jsx";
import CardView from "./util/CardView.jsx";
import DropdownButton from 'react-bootstrap/DropdownButton';
import {Box, Skeleton} from "@mui/material";
import('./threat.scss')
import('../../scss/util.scss')


const Threat = ({primaryInfo, infoForCardView, otherImportantInfo, fetchDataFunction}) => {
    const [searchedResult, setSearchedResult] = useState(null);
    // const location = useLocation();
    const idObj = new URLSearchParams(useLocation().search).get('id');

    const [infoForCardViewDict, setInfoForCardViewDict] = useState(null);
    const [otherImportantInfoDict, setOtherImportantInfo] = useState(null);
    const [otherInfoDict, setOtherInfoDict] = useState()
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        // const idObj = location.state.id;
        setLoading(true)
        const root_element = document.getElementById('root');
        root_element.classList.add('scrollbar')

        // FETCH DATA FROM API
        fetchDataFunction(idObj).then((r) => {
            setSearchedResult(r.data);
            setLoading(false)
        });
    } , []);

    // SET OTHER IMPORTANT INFO DICT
    useEffect(() => {
        if (searchedResult) {
            var newDict = {};

            // create dict of important info (for card info in view)
            for (let key of infoForCardView) {
                if (searchedResult.hasOwnProperty(key)) {
                    newDict[key] = searchedResult[key];
                }
            }
            setInfoForCardViewDict(newDict)

            // create dict of other important info
            newDict = {}
            for (let key of otherImportantInfo) {
                if (searchedResult.hasOwnProperty(key)) {
                    newDict[key] = searchedResult[key];
                }
            }
            setOtherImportantInfo(newDict)

            // create dict of other info
            const keysToExclude = [...otherImportantInfo, ...infoForCardView, ...primaryInfo];
            newDict = {};
            for (let key in searchedResult) {
                if (searchedResult.hasOwnProperty(key) && !keysToExclude.includes(key)) {
                    newDict[key] = searchedResult[key];
                }
            }
            setOtherInfoDict(newDict)

        }
    }, [searchedResult]);

    return (
        <div className="container-fluid  px-lg-5 pb-3">

            {loading ? (
                <>
                    <div className="row mb-0">
                        <div className="col mt-5 " >
                            {/*Name*/}
                            <Skeleton className="col-9 mt-4" animation="wave" variant="rounded" height={100} />
                            {/*Type*/}
                            <Skeleton className="col-2 mt-3" animation="wave" variant="rounded" height={60} />
                            {/*Description*/}
                            <Skeleton className="mt-5 me-5" animation="wave" variant="rounded" height={500} />
                        </div>
                        {/*CardView*/}
                        <Skeleton className="col-2 me-3" animation="wave" variant="rounded" height={400}  />

                    </div>
                </>
            ) : (
                searchedResult && otherImportantInfoDict && (
                    <>
                        <div className="row align-items-end">
                            <div className="col">
                                <ImportantInfo importantInfoDict={searchedResult}/>

                                {
                                    Object.keys(otherInfoDict).length !== 0 &&(
                                        <DropdownButton title='Other info' variant="Secondary" drop="end" className="">
                                            <div className="dropdown-my-content"><RenderDict infoDict={otherInfoDict}/></div>
                                        </DropdownButton>
                                    )
                                }

                            </div>
                            <div className="col-3  mb-auto margin-top-100">
                                <CardView infoDict={infoForCardViewDict}/>
                            </div>
                        </div>
                        {
                            otherImportantInfoDict && (
                                <div className="ms-5">

                                    <OtherImportantInfo otherImportantInfoDict={otherImportantInfoDict}/>
                                    {/*<RenderDict infoDict={otherInfoDict}/>*/}
                                </div>
                            )
                        }
                    </>
                )
            )
            }


        </div>
    );
}

export default Threat;
