import React from "react";
import "./header.css"
import Navbar_ from "./navbar/Navbar_.jsx";
import {ThemeProvider} from "react-bootstrap";
import ThemeSwitch from "../theme_switch/themeSwitch.jsx";
const Header = () => {
    return (
        <div>
            <Navbar_/>
            <ThemeSwitch/>
        </div>
    );
}

export default Header;