import React, {useEffect} from 'react';
import { Link } from 'react-router-dom';
import search_lens from '../../assets/search_lens.png';
import './searching_choice.scss';
import FilePicker from "../../components/file_picker/filePicker.jsx";

function SearchingChoice() {

    useEffect(() => {
        const root_element = document.getElementById('root');
        root_element.classList.add('d-flex')
        root_element.classList.add('align-content-center')
        root_element.classList.add('justify-content-center')
        root_element.classList.add('align-items-center')
        root_element.style.margin = "0 auto";
        root_element.style.height = "100.1vh";
    });

    return (
        <div style={{marginTop: '40px'}}>
            <div className="container text-center title">
                <h1 className="display-4 fw-bolder text-primary">Choose your searching method:</h1>
            </div>

            <div className="container text-center">
                <div className="row">
                    <div className="col justify-content-center">
                        <h3 className="fw-bold">UPLOAD REPORT</h3>
                        <p className="mt-2 text-secondary">
                            Here you can upload a report with .pdf or .txt, that contains a CWEs or CVEs id in text!</p>
                        <div id="file-picker-placeholder">
                            <FilePicker/>
                        </div>
                    </div>

                    <div className="d-flex col-1 justify-content-center align-items-center" style={{height: 'auto'}}>
                        <div className="vr thick-vr border-primary"></div>
                    </div>

                    <div className="col justify-content-center">
                        <h3 className="fw-bold">MANUAL SEARCH</h3>
                        <p className="mt-2 text-secondary">Choose manual searching to explore the system in manual mode!</p>
                        <div className="row justify-content-center">
                            <img className="lens" src={search_lens} alt="lens"/>
                        </div>
                        <div className="row mt-3">
                            <Link to="/manual_search">
                                <button type="button" className="btn btn-outline-primary fw-semibold v">Start search</button>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default SearchingChoice;