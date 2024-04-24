import React, {useState} from 'react';
import DropdownButton from './DropdownButton.jsx';
import RenderList from './RenderList';

function RenderDict({ itemDict }) {
  const [dropdownStates, setDropdownStates] = useState({});

  const toggleDropdown = (key) => {
    setDropdownStates(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <>
      {Object.entries(itemDict).map(([key, value], index) => {
        const uniqueKey = `${key.replace(/\s/g, '_')}${index}`;
        return (
          <div key={uniqueKey}>
            <p>
              <span className="text-secondary display-6 fs-6 me-2 h5">{key}:</span>
              {Array.isArray(value) ? (
                <>
                  <DropdownButton id={uniqueKey} upOrDown={dropdownStates[uniqueKey]} toggleDropdown={() => toggleDropdown(uniqueKey)} />
                  <div className={dropdownStates[uniqueKey] ? 'ms-5 show' : 'ms-5 hide'}>
                    <RenderList itemList={value} />
                  </div>
                </>
              ) : (
                key === 'URL' ? <a href={value} target="_blank">{value}</a> : <span>{value}</span>
              )}
            </p>
            <Line shouldDraw={key !== 'URL'} />
          </div>
        );
      })}
    </>
  );
}

export default RenderDict;
