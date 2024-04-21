import React, { useState, useEffect } from "react";
import "./scroll_anim.css";
import "./home.css";
import "../../scss/util.scss"
import cyber from "../../assets/cyber.png";
import { scrollHideWhileDown, scrollHideWhileUp, scrollHideWhileDownMouse, scrollHideWhileUpDescription } from "./scrollAnim.js";

const Home = () => {
    const [showLogo, setShowLogo] = useState(true);
    const [showMouse, setShowMouse] = useState(true);
    const [showDescription, setShowDescription] = useState(false);

    const handleScroll = () => {
        scrollHideWhileDownMouse();
        scrollHideWhileUpDescription();
        scrollHideWhileUp('.small-logo');
        scrollHideWhileDown('.big-logo');
    };

    useEffect(() => {
        window.addEventListener("scroll", handleScroll);
    }, []);

    return (
        <div className="container-fluid big-logo-container d-flex flex-column justify-content-center align-items-center">
            <div className={`container-fluid justify-content-center transition-element`}>
                <h1 className="big-logo">Detective Attack</h1>
            </div>
            <div className="d-flex justify-content-center align-items-center sub-title">
                <h2 className="mb-0 display-2 sub-title text-primary transition-element">Prevent attacks in your business</h2>
            </div>

            <div className={`container-fluid d-flex justify-content-center align-items-center mb-5 mouse`}></div>

            <div className={`container-fluid transition-element description hide`}>
                <div className="row justify-content-center align-items-center">
                    <div className="col-md-6 justify-content-center text-center">
                        <div className="text-description">
                            <p>Dolor sit amet, consectetur adipisicing elit. Id, sapiente. Dolor sit amet, consectetur adipisicing elit. Id, sapiente. Dolor sit amet, consectetur adipisicing elit. Id, sapiente.</p>
                            <p>Dolor sit amet, consectetur adipisicing elit. Id, sapiente.</p>
                            <div className="row justify-content-center align-items-center text-center">
                                <a className="text-decoration-none" href="searching_choice">
                                    <button type="button" className="btn btn-outline-primary fs-5 fw-bolder mt-2 shadow">
                                        Get started
                                    </button>
                                </a>
                            </div>
                        </div>
                        <div className="row justify-content-center align-items-center">
                            <img src={cyber} className="cyber-img mt-xl-5" alt="Cybersecurity Logo"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};


export default Home;
