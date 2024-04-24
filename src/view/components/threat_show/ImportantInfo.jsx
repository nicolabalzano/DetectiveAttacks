import React from "react";

function ImportantInfo({importantInfoDict}){

    // render of Name, Type and Description
    return (
        <>
            <div className="text-primary display-3">
                {importantInfoDict['Name']}
                <p className="text-secondary fs-4 mt-3">
                    {importantInfoDict.Type}
                </p>
            </div>
            <p className="fs-5">{importantInfoDict['Description']}</p>
        </>
    );
}

export default ImportantInfo;