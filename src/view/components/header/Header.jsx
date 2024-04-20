import React from "react";
import "./header.css"
import Navbar from "./navbar/Navbar.jsx";
import {ThemeProvider} from "react-bootstrap";
import ThemeSwitch from "../theme_switch/themeSwitch.jsx";
const Header = () => {
    return (
        <div>
            <Navbar/>

        </div>
    );
}

export default Header;