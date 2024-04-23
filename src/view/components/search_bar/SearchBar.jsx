import React, { useState, useRef } from 'react';
import './search_bar.scss';


const SearchBar = ({ onSearch, finderRef }) => {
  const inputRef = useRef(null);

  const handleFocus = () => {
    finderRef.current.classList.add("active");
  };

  const handleBlur = () => {
    if (inputRef.current.value.length === 0) {
      finderRef.current.classList.remove("active");
    }
  };

  const handleSearch = (ev) => {
    ev.preventDefault();
    finderRef.current.classList.add("processing");
    finderRef.current.classList.remove("active");
    setTimeout(() => {
      finderRef.current.classList.remove("processing");
      inputRef.current.disabled = false;
      if (inputRef.current.value.length > 0) {
        finderRef.current.classList.add("active");
      }
      onSearch(inputRef.current.value);
    }, 1000);
  };

  return (
    <div className="finder" ref={finderRef}>
      <div className="finder__outer">
        <div className="finder__inner">
          <div className="finder__icon" ref={inputRef}></div>
          <form onSubmit={handleSearch}>
            <input
              className="finder__input text-light"
              type="search"
              id="input_search_bar"
              name="search"
              placeholder="Search threats..."
              ref={inputRef}
              onChange={handleSearch}
              onFocus={handleFocus}
              onBlur={handleBlur}
            />
          </form>
        </div>
      </div>
    </div>
  );
};

export default SearchBar;