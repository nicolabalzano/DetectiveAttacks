import React, {useState} from 'react';
import RenderList from './RenderList';
import Line from "./Line.jsx";
import {navigateToThreats} from "../../../pages/manual_search/HandleRoutingThreats.jsx";

function RenderDict({ infoDict }) {

  return (
    <>
      {Object.entries(infoDict).map(([key, value], index) => {
        const uniqueKey = `${key.replace(/\s/g, '_')}${index}`;
        return (
          <div key={uniqueKey}>
            <p className="mb-2">
              <span className="text-secondary display-6 fs-6 me-2 h5 fw-semibold">{key}:</span>
              {Array.isArray(value) ? (
                <>
                    <RenderList itemList={value}/>
                </>
              ) : (
                  key === 'URL'
                      ?
                      <a href={value} target="_blank">{value}</a>
                      :
                      key.includes('ID')
                          ?
                          <span className="fs-6 text-decoration-underline link-primary
                            link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover"
                                role="button"
                                onClick={() => navigateToThreats(value)}>{value}</span>
                          :
                          <span>{value}</span>
              )}
            </p>
          </div>
        );
      })}
    </>
  );
}

export default RenderDict;
