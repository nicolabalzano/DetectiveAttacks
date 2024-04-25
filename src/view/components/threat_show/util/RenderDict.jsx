import React, {useState} from 'react';
import RenderList from './RenderList';
import Line from "./Line.jsx";

function RenderDict({ infoDict }) {
  /*
  const [dropdownStates, setDropdownStates] = useState({});

  const toggleDropdown = (key) => {
    setDropdownStates(prev => ({ ...prev, [key]: !prev[key] }));
  };
*/

  return (
    <>
      {Object.entries(infoDict).map(([key, value], index) => {
        const uniqueKey = `${key.replace(/\s/g, '_')}${index}`;
        return (
          <div key={uniqueKey}>
            <p>
              <span className="text-secondary display-6 fs-6 me-2 h5 fw-semibold">{key}:</span>
              {Array.isArray(value) ? (
                <>
                    <RenderList itemList={value}/>
                </>
              ) : (
                  key === 'URL' ? <a href={value} target="_blank">{value}</a> : <span>{value}</span>
              )}
            </p>
          </div>
        );
      })}
    </>
  );
}

export default RenderDict;
