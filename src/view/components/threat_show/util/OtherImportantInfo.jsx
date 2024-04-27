import React, {useEffect, useState} from 'react';
import RenderList from './RenderList';
import DropdownButton from 'react-bootstrap/DropdownButton';
import {navigateToThreats} from "../../../pages/manual_search/HandleRoutingThreats.jsx";
import RenderDict from "./RenderDict.jsx";
import Line from "./Line.jsx";

function handleDropdown(e) {
    const dropdown_id = e.target.id;
    const id = dropdown_id+'_div';
    const element = document.getElementById(id);
    const dropdown = document.getElementById(dropdown_id);
    if (element.classList.contains('d-none')) {
        element.classList.remove('d-none');
        dropdown.classList.add('bi-caret-up-fill');
        dropdown.classList.remove('bi-caret-down-fill');
    } else {
        element.classList.add('d-none');
        dropdown.classList.remove('bi-caret-up-fill');
        dropdown.classList.add('bi-caret-down-fill');
    }
}

function RenderValue({ subDict }) {
    const primaryInfo = ['Name', 'ID', 'Description'];
    const [subOtherImportantInfo, setSubOtherImportantInfo] = useState({});

    useEffect(() => {

        // delete manual rendered info from subDict
        let newDict = {};
        for (let key in subDict) {
            if (!primaryInfo.includes(key)) {
                newDict[key] = subDict[key];
            }
        }
        setSubOtherImportantInfo(newDict);

    }, [subDict]); // Depends on subDict


    return (
        <>
            {JSON.stringify(Object.keys(subDict).sort()) === JSON.stringify(Object.keys(subOtherImportantInfo).sort())

                ? // If it's an array like Related Attack Patterns to show Phases
                (
                    Object.entries(subDict).map(([subTitle, subValue], subIndex) => (
                        <p className="ms-5">
                            <span className="display-6 fs-3">{subTitle} </span>
                            <span> <i className="bi bi-caret-down-fill" role="button" id={subTitle}
                                      onClick={(e) => handleDropdown(e)}></i></span>

                            <div className="d-none" id={subTitle + '_div'}>
                                {Array.isArray(subValue) ?
                                    subValue.map((subSubDict, subIndex) => (
                                        <>
                                            {(()=>{
                                                // delete manual rendered info from subDict (Name and Description, and Type but is used only to generate clickable ID link)
                                                const { Name, Description, Type, ...dictWithNoNameAndDescription } = subSubDict;
                                                return <div className="ms-5 mt-3">
                                                    <p className="">{Name}</p>
                                                    <p className="">{Description}</p>
                                                    <RenderDict infoDict={dictWithNoNameAndDescription}/>
                                                    <Line/>
                                                </div>;
                                            })()}
                                        </>
                                    ))
                                    :
                                    <div>{subValue}</div>
                                }
                            </div>

                        </p>
                    ))
                )

                : // If it's a normal object
                (
                    < div className="ms-5">
                        <p>
                            {/*Name*/}
                            <span className="display-6 fs-3">{subDict.Name} </span>

                            {/*ID*/
                            }
                            {
                                // if ID is not empty and Type does not contain 'course-of-action' (for Mitigations), then it is a link
                                subDict.ID && subDict.Type && !subDict.Type.includes('course-of-action') ? (
                                    <>
                                        <span className="text-secondary fs-6">(</span>
                                        <span className="fs-6 text-decoration-underline link-primary
                            link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover"
                                              role="button" onClick={() => navigateToThreats(subDict.ID, subDict.Type)}>{subDict.ID}</span>
                                        <span className="text-secondary fs-6">)</span>
                                    </>
                                ) : (
                                    <>
                                        <span className="text-secondary fs-6">(</span>
                                        <span className="fs-6 text-secondary">{subDict.ID}</span>
                                        <span className="text-secondary fs-6">)</span>
                                    </>
                                )
                            }
                            <span> <i className="bi bi-caret-down-fill" role="button" id={subDict.Name} onClick={(e) => handleDropdown(e)}></i></span>
                        </p>

                        {/*Info*/
                        }
                        <div className="ms-3 mb-3 d-none" id={subDict.Name + '_div'}>

                            {/*Description*/}
                            {
                                subDict.Description && (<p>{subDict.Description}</p>)
                            }

                            { // Other info
                                subOtherImportantInfo && (
                                    Object.entries(subOtherImportantInfo).map(([subTitle, subValue], subIndex) => (
                                        <div key={subIndex} className="mb-2">

                                            {
                                                Array.isArray(subValue)
                                                    ? // If it's an array
                                                    <>
                                                        <DropdownButton title={subTitle} variant="Secondary" drop="end">
                                                            <div className="dropdown-my-content">
                                                                <RenderList itemList={subValue}/>
                                                            </div>
                                                        </DropdownButton>
                                                    </>
                                                    : // If it's not an array
                                                    <>
                                                        <span className="text-secondary fs-6 fw-semibold">{subTitle}: </span>
                                                        <span className="text-secondary fs-6">{subValue}</span>
                                                    </>
                                            }


                                        </div>
                                    ))
                                )
                            }
                        </div>
                    </div>
                )
            }
        </>
    );
}

function OtherImportantInfo({ otherImportantInfoDict }) {
    return (
        <>
            {Object.entries(otherImportantInfoDict).map(([title, value], index) => (
                <div key={index}>
                    <p className="text-primary display-6 fs-3 mt-4">{title}
                        <span> <i className="bi bi-caret-down-fill fs-5" role="button" id={title}
                                  onClick={(e) => handleDropdown(e)}></i></span>
                    </p>
                    <div className="d-none" id={title + '_div'}>
                        {Array.isArray(value) ?
                            value.map((subDict, subIndex) => (
                                <RenderValue key={subIndex} subDict={subDict} />
                            ))
                            :
                            <div>{value}</div>
                        }
                    </div>
                </div>
            ))}
        </>
    );
}

export default OtherImportantInfo;
