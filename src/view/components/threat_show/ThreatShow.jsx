import React from 'react';
import RenderDict from './RenderDict';

function ThreatShow({ data }) {
  return (
    <div>
      {Object.entries(data).map(([key, value], index) => (
        <RenderDict key={index} itemDict={{ [key]: value }} />
      ))}
    </div>
  );
}

export default ThreatShow
