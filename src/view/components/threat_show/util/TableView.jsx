import {navigateToThreats} from "../../../pages/manual_search/HandleRoutingThreats.jsx";
import React from "react";
import {useState} from "react";

const TableView = ({ infoList }) => {
    const [colorMapSource, setColorMapSource] = useState({})

    function generateRandomColor() {
        const red = Math.floor(Math.random() * 256);
        const green = Math.floor(Math.random() * 256);
        const blue = Math.floor(Math.random() * 256);
        return `rgb(${red}, ${green}, ${blue})`;
    }

    function getColorForSource(source){
        if (source in colorMapSource){
            return colorMapSource[source];
        } else {
            colorMapSource[source] = generateRandomColor();
            setColorMapSource(colorMapSource);
            return colorMapSource[source];
        }
    }

    return (
        <div className="row d-flex justify-content-center">
            <div className="fw-bold">Source of relationship:</div>
            <div className="mb-3 mt-1">
                {
                    Object.entries(colorMapSource).map(([key, value]) => (
                        <div key={key} className="d-inline-block justify-content-start">
                            <span className=" m-0 ms-1 ms-4 text-decoration-underline link-primary
                            link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover"
                                  role="button"
                                  onClick={() => navigateToThreats(key)}>{key}</span>
                            <span className=" d-inline-block ms-1"
                                  style={{background: value, width: '10px', height: '10px'}}> </span>
                        </div>
                    ))
                }
            </div>
            {
                Array.isArray(infoList) ?
                    infoList.map((subDict, subIndex) => (
                        Object.entries(subDict).map(([key, value]) => (
                            <div key={key} className="col p-0 text-center text-break">
                                <p className="m-0 py-2 border border-secondary">
                                    <span className="fw-semibold fs-6 ">{key} </span>
                                </p>
                                {
                                    Array.isArray(value) ?
                                        value.map((subDict, subIndex) => (
                                            <div className=" m-0 border-bottom border-start border-end border-secondary py-2  "
                                                 style={{fontSize: '12px'}}>
                                                {subDict['Attack name']}
                                                <p className="text-decoration-underline link-primary
                            link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover m-0"
                                                   role="button"
                                                   onClick={() => navigateToThreats(subDict['ID'])}>{subDict['ID']}</p>
                                                <div className="d-flex justify-content-end me-1">
                                                    <div style={{
                                                        background: getColorForSource(subDict['Relationship Source ID']),
                                                        width: '10px',
                                                        height: '10px'
                                                    }}></div>
                                                </div>
                                            </div>

                                        ))
                                        : null
                                }
                            </div>
                        ))

                    )) :
                    <div>{value}</div>

            }
        </div>
    );

}

export default TableView;