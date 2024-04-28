import React, {useEffect, useState} from 'react';
import RenderDict from './util/RenderDict';
import {useLocation, useParams} from "react-router-dom";
import {fetchDataAttackAPI} from "../api/fetchAPI.jsx";
import ImportantInfo from "./util/ImportantInfo.jsx";
import OtherImportantInfo from "./util/OtherImportantInfo.jsx";
import CardView from "./util/CardView.jsx";
import DropdownButton from 'react-bootstrap/DropdownButton';
import('./threat.scss')


const Threat = ({primaryInfo, infoForCardView, otherImportantInfo, fetchDataFunction}) => {
    const [searchedResult, setSearchedResult] = useState(null);
    // const location = useLocation();
    const idObj = new URLSearchParams(useLocation().search).get('id');

    const [infoForCardViewDict, setInfoForCardViewDict] = useState(null);
    const [otherImportantInfoDict, setOtherImportantInfo] = useState(null);
    const [otherInfoDict, setOtherInfoDict] = useState()


    useEffect(() => {
        // const idObj = location.state.id;

        // FETCH DATA FROM API
        fetchDataFunction(idObj).then((r) => {
            setSearchedResult(r.data);
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
            {searchedResult && otherImportantInfoDict && (
                <>
                    <div className="row align-items-end">
                        <div className="col">
                            <ImportantInfo importantInfoDict={searchedResult}/>

                            {
                                Object.keys(otherInfoDict).length !== 0 &&(
                                    <DropdownButton title='Other info' variant="Secondary" drop="end" className="mt-3">
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
            )}
        </div>
    );
}

export default Threat;
