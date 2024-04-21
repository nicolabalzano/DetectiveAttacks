import React from 'react';
import './navbar.css';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import logo from '../../../assets/logo.svg'; // Importa l'immagine

const Navbar_ = () => {
    return (
        <Navbar className="navbar navbar-expand-lg navbar-inverse mb-5 bg-body ps-3 pe-3 " fixed="top">

            {/* LOGO */}
            <Navbar.Brand className="d-flex justify-content-center align-items-center me-auto">
                <a className="navbar-brand" href="/">
                    <img src={logo} alt="Logo" width="30" height="24" className="logo-img d-inline-block align-text-top" />
                </a>
            </Navbar.Brand>

            {/* SMALL TITLE */}
            <div className="d-flex justify-content-center align-items-center me-auto ms-auto">
                <div className="container-fluid d-flex justify-content-center align-items-center small-logo-container ">
                    <a className="small-logo h1 transition-element" href="/">Detective Attack</a>
                </div>
            </div>

            {/* MENU */}
            <Nav className="ms-auto">
                <Nav.Link className="collapse navbar-collapse container-fluid align-items-center me-auto">
                    <a className="nav-link text-primary" href="searching_choice">About</a>
                </Nav.Link>
            </Nav>

        </Navbar>
    );
}

export default Navbar_;