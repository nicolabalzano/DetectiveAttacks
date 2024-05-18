import React from "react";
import "./header.css"
import Navbar_ from "./navbar/Navbar_.jsx";
import {ThemeProvider} from "react-bootstrap";
import ThemeSwitch from "../theme_switch/ThemeSwitch.jsx";
import {Outlet} from "react-router-dom";
const Header = () => {
    return (
        <div>
            <ThemeSwitch/>
            <Navbar_/>
            <Outlet/>
        </div>
    );
}

export default Header;