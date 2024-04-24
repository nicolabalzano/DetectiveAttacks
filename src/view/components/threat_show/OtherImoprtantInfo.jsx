import React, {useEffect, useState} from 'react';
import DropdownButton from './DropdownButton.jsx';
import RenderList from './RenderList';
import Line from './Line';



function renderValue(subDict) {
    const primaryInfo = ['Name', 'ID', 'Description'];
    const subOtherImportantInfo = {};
    const [dropdownStates, setDropdownStates] = useState({});

    useEffect(() => {
        for (let key of primaryInfo) {
            // remove manual rendered info from dict
            if (subDict.hasOwnProperty(key)) {
                subOtherImportantInfo[key] = subDict[key];
            }
        }
    }, []);

    return (
        <div className="ms-5" key={index}>
            <p>
                <span className="display-6 fs-3">{subDict.Name}</span>
                <span className="text-secondary fs-6">({subDict.ID})</span>
            </p>
            <div className="ms-3">
                <p>{subDict.Description}</p>
            </div>
            {
                Object.entries(subOtherImportantInfo).map(([subTitle, subValue], subIndex) => (
                    <div key={subIndex}>
                        <span className="text-secondary fs-6 fw-semibold">{subTitle}:</span>
                        {Array.isArray(subValue)
                            ? /* If it's a list */
                            <div>
                                <DropdownButton id={subTitle + subIndex}
                                                upOrDown={true}
                                                toggleDropdown={() => setDropdownStates({...dropdownStates,[subTitle + subIndex]: !dropdownStates[subTitle + subIndex]
                                                })}/>
                                {
                                    dropdownStates[subTitle + subIndex] && (
                                        <div>
                                            <RenderList itemList={subValue}/>
                                            <Line shouldDraw={true}/>
                                        </div>
                                    )}
                            </div>
                            : /* If is not a list */
                            <span className="text-secondary fs-6 fw-semibold">{subValue}</span>
                        }
                    </div>
                ))
            }
        </div>
    )
}

function OtherImportantInfo({ otherImportantInfoDict}) {

    // console.log(otherImportantInfoDict)
    return (
        <>
            {
                Object.entries(otherImportantInfoDict).map(([title, value], index) => (
                    <div className="ms-5" key={index}>
                        <p className="text-primary display-6 fs-3">{title}</p>
                        <div>

                            {/* If it's a list */}
                            Array.isArray(value) ?

                            {/* Render each dict in the list */}
                            value.map((subDict, subIndex) => (
                                <div key={subIndex}>{renderValue(subDict)}</div>
                            ))

                            : {/* If is not a list */}
                            <div>{value}</div>
                        </div>

                    </div>
                ))
            }
        </>
    )
        ;
}

export default OtherImportantInfo;
