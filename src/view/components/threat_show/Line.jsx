import React from 'react';

function Line({ shouldDraw }) {
  return shouldDraw ? <hr className="border border-1 border-primary shadow rounded " /> : null;
}

export default Line;