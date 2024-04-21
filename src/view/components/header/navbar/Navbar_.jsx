import React from 'react';
import './navbar.css';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';

const Navbar_ = () => {
    return (
        <Navbar className="navbar navbar-expand-lg navbar-inverse fixed-top mb-5 bg-body">

            {/* LOGO */}
            <Navbar.Brand className="d-flex align-items-center ms-auto">
                <a className="navbar-brand" href="/">
                    <img src="../../../assets/logo.svg" alt="Logo" width="30" height="24" className="logo-img d-inline-block align-text-top" />
                </a>
            </Navbar.Brand>

            {/* SMALL TITLE */}
            <div className="container-fluid d-flex justify-content-center align-items-center small-logo-container ms-auto">
                <a className="small-logo h1" href="/">Attack Prediction Tool</a>
            </div>

            {/* MENU */}
            <Nav className="me-auto">
                <Nav.Link className="collapse navbar-collapse container-fluid align-items-center me-auto">

                    <a className="nav-link text-primary" href="searching_choice">About</a>
                </Nav.Link>
            </Nav>

        </Navbar>
    );
}

export default Navbar_;