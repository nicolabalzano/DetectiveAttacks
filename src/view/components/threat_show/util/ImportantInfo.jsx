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
            {
                importantInfoDict.Description &&
                <div className="text-secondary fs-5 mt-3">
                    {importantInfoDict.Description}
                </div>
            }
        </>
    );
}

export default ImportantInfo;