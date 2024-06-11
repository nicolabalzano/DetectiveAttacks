import React from 'react';
import './navbar.css';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import LogoSvg from "../../../assets/LogoSvg.jsx";
import Menu from "../../lateral_menu/Menu.jsx";

const Navbar_ = () => {
    return (
        <Navbar className="navbar navbar-expand-lg navbar-inverse bg-body ps-3 pe-3" fixed="top">

            {/* LOGO Company*/}
            <Navbar.Brand className="d-flex justify-content-center align-items-center me-auto">
                <span className="text-color display-6 fs-5" href="/">
                    NB Creations
                </span>
            </Navbar.Brand>

            {/* SMALL TITLE */}
            <div className="d-flex justify-content-center align-items-center me-auto ms-auto">
                <div className="container-fluid d-flex justify-content-center align-items-center small-logo-container small-logo transition-element">
                    <a className="h1 m-0 text-decoration-none" href="/">DetectiveAttacks</a>
                    <LogoSvg w={'50px'} h={'50px'}/>

                </div>
            </div>

            {/* ABOUT */}
            <Nav className="ms-auto">
                <Nav.Link className="collapse navbar-collapse container-fluid align-items-center me-auto">
                    <Menu/>               
                </Nav.Link>
            </Nav>

        </Navbar>
    );
}

export default Navbar_;