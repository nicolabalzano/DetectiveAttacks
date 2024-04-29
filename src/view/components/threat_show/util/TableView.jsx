import {navigateToThreats} from "../../../pages/manual_search/HandleRoutingThreats.jsx";
import React from "react";

const TableView = ({ infoDict }) => {


    return (
        <div className="col p-0">
            {
                Object.entries(infoDict).map(([key, value]) => (
                    <div key={key} className="border border-secondary px-1 text-center text-break">
                        <p className="m-0 py-2 ">
                            <span className="fw-semibold fs-6 ">{key} </span>
                        </p>
                        {
                            Array.isArray(value) ?
                                value.map((subDict, subIndex) => (
                                    <div className="border-top border-secondary py-2  " style={{fontSize: '12px'}}>
                                        {subDict['Attack name']}
                                        <p className="text-decoration-underline link-primary
                            link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover m-0"
                                              role="button"
                                              onClick={() => navigateToThreats(subDict['ID'])}>{subDict['ID']}</p>
                                    </div>

                                ))
                                :
                                <div>{value}</div>
                        }
                    </div>
                ))
            }
        </div>
    );

}

export default TableView;