import React, { useState, useEffect } from "react";
import "./scroll_anim.css";
import "./home.css";
import "../../scss/util.scss"
import cyber from "../../assets/cyber.png";
import {handleScroll} from "./scrollAnim.js";
import {Link} from "react-router-dom";
import LogoSvg from "../../assets/LogoSvg.jsx";

const Home = () => {

    useEffect(() => {
        const root_element = document.getElementById('root');
        root_element.classList.add('d-flex')
        root_element.classList.add('align-content-center')
        root_element.classList.add('justify-content-center')
        root_element.classList.add('align-items-center')
        root_element.style.margin = "0 auto";
        root_element.style.height = "100.1vh";


        document.querySelector('.small-logo').classList.add('hide');

        window.addEventListener("scroll", handleScroll);

      // Clean up the event listener when the component unmounts
        return () => {
            window.removeEventListener("scroll", handleScroll);
      };
    }, []);

    return (
        <div className="container-fluid big-logo-container d-flex flex-column justify-content-center align-items-center first-container no-scrollbar text-center">
            <div className={`container-fluid justify-content-center transition-element`}>
                <h1 className="big-logo fw-bolder">DetectiveAttacks
                <LogoSvg w={'180px'} h={'180px'}/></h1>
            </div>
            <div className="d-flex justify-content-center align-items-center sub-title">
                <h2 className="mb-0 display-2 sub-title text-primary transition-element">Prevent attacks in your business</h2>
            </div>

            <div className={`container-fluid d-flex justify-content-center align-items-center mouse`}></div>

            <div className={`container-fluid transition-element description hide`}>
                <div className="row justify-content-center align-items-center">
                    <div className="col-md-6 justify-content-center text-center">
                        <div className="text-description lead fs-5">
                            <p className="m-0 mb-1">DetetectiveAttacks is a tool that lets you explore knowledge of <b>CTI</b> including <b>CVE</b>, <b>CWE</b>, <b>attack patterns</b>, <b>mitigations</b>, <b>assets</b>, <b>tools</b>, <b>malware</b>, <b>campaigns</b> and <b>intrusion</b> sets from the <b>Enterprise</b>, <b>Mobile</b>, <b>ICS</b> and <b>AML</b> domains.
                                </p>
                                <p className="m-0 ">It allows to obtain the <b>relationships</b> between the various objects, providing detection and mitigation suggestions for specific cases and the possibility to learn the vulnerabilities through procedures examples. </p>
                                <p>By selecting the attack patterns found it is possible to get a <b>report</b> that indicates the probability with which you are suffering an attack by the known threat agents/groups</p>
                            <div className="row justify-content-center align-items-center text-center">
                                <Link to="searching_choices">
                                    <button type="button" className="btn btn-outline-primary fs-5 fw-bolder mt-2 shadow">
                                        Get started
                                    </button>
                                </Link>
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
