import React from 'react';

function DropdownButton({ id, upOrDown, toggleDropdown }) {
  return (
    <span className="text-secondary align-middle opacity-75" role="button" onClick={() => toggleDropdown(id)}>
      {upOrDown ? <i className="bi bi-caret-up"></i> : <i className="bi bi-caret-down"></i>}
    </span>
  );
}

export default DropdownButton;
