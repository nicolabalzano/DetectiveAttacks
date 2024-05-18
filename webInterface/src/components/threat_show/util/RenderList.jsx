import React from 'react';
import RenderDict from './RenderDict';
import Line from "./Line.jsx";

function RenderList({ itemList }) {
  return (
      <>
        {itemList.map((item, index) => (
            <div key={index} className="px-lg-2 mt-2 ">
              {Array.isArray(item) ?
                  <RenderList itemList={item} />
                  :
                  <>
                    <RenderDict infoDict={item} />
                    {(itemList.length - 1 !== index) &&
                        <Line/>
                    }
                  </>
              }
            </div>
        ))}
      </>
  );
}

export default RenderList;
