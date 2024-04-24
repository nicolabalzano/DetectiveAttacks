import React, { useState } from 'react';
import DropdownButton from './DropdownButton.jsx';
import RenderList from './RenderList';
import Line from './Line';

function RenderProcedureExamples({ procedureExamples }) {
  const [dropdownStates, setDropdownStates] = useState({});

  return (
      <>
        <p className="text-primary display-6 fs-3">Procedures examples</p>
        {procedureExamples.map((example, index) => (
            <div className="ms-5" key={index}>
              <p>
                <span className="display-6 fs-3">{example.Name}</span>
                <span className="text-secondary fs-6">({example.ID})</span>
              </p>
              <div className="ms-3">
                <p>{example.Description}</p>
                <p className="text-secondary fs-6"><strong>Purpose:</strong> {example.Purpose}</p>
                <p className="text-secondary fs-6"><strong>Suggestion for this
                  case:</strong> {example['Suggestion for this case']}</p>
                <p className="text-secondary fs-6">
                  <strong>External references:</strong>
                  <DropdownButton id={'externalReferences' + index}
                                  upOrDown={dropdownStates['externalReferences' + index]}
                                  toggleDropdown={() => setDropdownStates({
                                    ...dropdownStates,
                                    ['externalReferences' + index]: !dropdownStates['externalReferences' + index]
                                  })}/>
                  {dropdownStates['externalReferences' + index] && (
                      <div>
                        <RenderList itemList={example['External references']}/>
                      </div>
                  )}
                </p>
              </div>
              <Line shouldDraw={true}/>
            </div>
        ))}
      </>
  );
}

export default RenderProcedureExamples;
