import React from "react";

function ImportantInfo({importantInfoDict}){

    // set the title of page
    document.title = importantInfoDict['Name'] + " " + importantInfoDict.Type + " " + importantInfoDict['ID'] ;

    // render of Name, Type and Description
    return (
        <>
            <div className="text-primary display-3 margin-top-100">
                {importantInfoDict['Name']}
                <p className="text-secondary fs-4 mt-3">
                    {importantInfoDict.Type}
                </p>
            </div>
            {
                importantInfoDict['Description'] &&
                <div className="fs-5 mt-3">
                    {importantInfoDict['Description']}
                </div>
            }
        </>
    );
}

export default ImportantInfo;