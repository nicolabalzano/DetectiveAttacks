import React from 'react';
import RenderDict from './RenderDict';
import Line from "./Line.jsx";

function RenderList({ itemList }) {
  return (
    <>
      {itemList.map((item, index) => (
        <span key={index} className="mt-2 ">
          {Array.isArray(item) ?
            <RenderList itemList={item} />
            :
            typeof item === 'string' ?
              <span>{item}</span>
              :
              <>
                <RenderDict infoDict={item} />
                {(itemList.length - 1 !== index) &&
                  <Line />
                }
              </>
          }
        </span>
      ))}
    </>
  );
}

export default RenderList;
