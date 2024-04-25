import React, {useEffect, useState} from 'react';
import RenderList from './RenderList';
import DropdownButton from 'react-bootstrap/DropdownButton';

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
        <div className="ms-5">
            <p>
                <span className="display-6 fs-3">{subDict.Name} </span>
                <span className="text-secondary fs-6">({subDict.ID})</span>
            </p>
            <div className="ms-3 mb-3">
                <p>{subDict.Description}</p>

                {
                    subOtherImportantInfo && (
                        Object.entries(subOtherImportantInfo).map(([subTitle, subValue], subIndex) => (
                            <div key={subIndex} className="mb-2">

                                {Array.isArray(subValue)
                                    ? <>
                                        <DropdownButton title={subTitle} variant="Secondary" drop="end" >
                                            <div className="dropdown-my-content">
                                                <RenderList itemList={subValue}/>
                                            </div>
                                        </DropdownButton>
                                    </>
                                    :
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
    );
}

function OtherImportantInfo({ otherImportantInfoDict }) {
    return (
        <>
            {Object.entries(otherImportantInfoDict).map(([title, value], index) => (
                <div key={index}>
                    <p className="text-primary display-6 fs-3 mt-4">{title}</p>
                    <div>
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
