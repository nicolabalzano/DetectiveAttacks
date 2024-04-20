import React from 'react';
import './navbar.css';

const Navbar = () => {
    return (
        <nav className="navbar navbar-expand-lg navbar-inverse fixed-top">

            {/* LOGO */}
            <div className="container-fluid d-flex align-items-center ">
                <a className="navbar-brand" href="/">
                    <img src="../../static/images/logo.svg" alt="Logo" width="30" height="24" className="logo-img d-inline-block align-text-top" />
                </a>
            </div>

            {/* SMALL TITLE */}
            <div className="container-fluid d-flex justify-content-center align-items-center ">
                <div className="small-logo-container">
                    <a className="small-logo h1" href="/">Attack Prediction Tool</a>
                </div>
            </div>

            {/* MENU */}
            <div className="collapse navbar-collapse container-fluid align-items-center">
                <div className="navbar-nav ms-auto">
                    <a className="nav-link text-primary" href="searching_choice">About us</a>
                </div>
            </div>

        </nav>
    );
}

export default Navbar;