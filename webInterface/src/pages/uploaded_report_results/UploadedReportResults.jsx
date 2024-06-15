import { useLocation } from 'react-router-dom';
import { useState } from 'react';
import { useEffect } from 'react';
import "../../scss/util.scss";

function UploadedReportResults() {

  const location = useLocation();
  const vulnerabilitiesLink = location.state || {};

  useEffect(() => {
    const root_element = document.getElementById('root');
    root_element.classList.add('d-flex')
    root_element.classList.add('align-content-center')
    root_element.classList.add('justify-content-center')
    root_element.classList.remove('align-items-center')
    root_element.style.margin = "0 auto";
    root_element.style.height = "100.1vh";
  });

  return (
    <>
      <div className='margin-top-100'>
        <div className="display-2 fw-bolder text-primary">Uploaded Report Results</div>
        <div className="mt-5 text-center display-5">Vulnerabilities found in the report:</div>
        <div className='display-6 mt-5 text-center'>
        {vulnerabilitiesLink && Object.keys(vulnerabilitiesLink).length > 0 && Object.entries(vulnerabilitiesLink).map(([vuln, link]) => {
            return (
                <span><a target='_blank' href={link}>{vuln}</a>, </span>
            )
          })}
        </div>
      </div>
    </>
  );
}

export default UploadedReportResults;