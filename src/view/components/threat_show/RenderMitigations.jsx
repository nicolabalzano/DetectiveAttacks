import React, { useState } from 'react';
import DropdownButton from './DropdownButton.jsx';
import RenderList from './RenderList';
import Line from './Line';

function RenderMitigations({ mitigations }) {
  const [dropdownStates, setDropdownStates] = useState({});

  return (
    <>
      {mitigations.map((mitigation, index) => (
        <div className="ms-5" key={index}>
          <p>
            <span className="display-6 fs-3">{mitigation.Name}</span>
            <span className="text-secondary fs-6">({mitigation.ID})</span>
          </p>
          <div className="ms-3">
            <p>{mitigation.Description}</p>
            <p className="text-secondary fs-6"><strong>Purpose:</strong> {mitigation.Purpose}</p>
            <p className="text-secondary fs-6"><strong>Suggestion for this case:</strong> {mitigation['Suggestion for this case']}</p>
            <p className="text-secondary fs-6">
              <strong>External references:</strong>
              <DropdownButton id={'externalReferences' + index} upOrDown={dropdownStates['externalReferences' + index]} toggleDropdown={() => setDropdownStates({ ...dropdownStates, ['externalReferences' + index]: !dropdownStates['externalReferences' + index] })} />
              {dropdownStates['externalReferences' + index] && (
                <div>
                  <RenderList itemList={mitigation['External references']} />
                </div>
              )}
            </p>
          </div>
          <Line shouldDraw={true} />
        </div>
      ))}
    </>
  );
}

export default RenderMitigations;
