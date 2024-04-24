import React from 'react';
import RenderDict from './RenderDict';

function RenderList({ itemList }) {
  return (
    <>
      {itemList.map((item, index) => (
        <div key={index} className="px-lg-2">
          {Array.isArray(item) ? <RenderList itemList={item} /> : <RenderDict itemDict={item} />}
        </div>
      ))}
    </>
  );
}

export default RenderList;
