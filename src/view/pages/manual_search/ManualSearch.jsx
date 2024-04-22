import React, {useEffect, useRef, useState} from 'react';
import SearchBar from "../../components/search_bar/SearchBar.jsx";
import axios from "axios";
import Pagination from "../../components/pagination/Pagination.jsx";
import './manual_search.scss';
import {TablePagination} from "@mui/material";

const ManualSearch = () => {
    const [searchTerm, setSearchTerm] = useState(null);
    const [list_of_filter_types, setListOfFilterTypes] = useState([]);
    const [list_of_filter_domains, setListOfFilterDomains] = useState([]);
    const [results, setResults] = useState([]);

    const [loading, setLoading] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [recordsPerPage] = useState(20);

    const indexOfLastRecord = currentPage * recordsPerPage;
    const indexOfFirstRecord = indexOfLastRecord - recordsPerPage;
    const currentRecords = results.slice(indexOfFirstRecord, indexOfLastRecord);
    const nPages = Math.ceil(results.length / recordsPerPage)

    const finderRef = useRef(null);

    const fetchAPI = async (searchTerm) => {
        console.log(import.meta.env.VITE_IP_PORT_TO_FLASK)
        setLoading(true);
        const response = await axios.get(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data/${searchTerm}`);
        setListOfFilterTypes(response.data.list_of_filter_types);
        setListOfFilterDomains(response.data.list_of_filter_domains);
        setResults(response.data.results);
        setLoading(false);
        console.log(response.data);
    };

    useEffect(() => {
        const root_element = document.getElementById('root');
        root_element.classList.remove('d-flex')
        root_element.classList.remove('align-content-center')
        root_element.classList.remove('justify-content-center')
        root_element.classList.remove('align-items-center')
        document.documentElement.style.margin = "0";
        fetchAPI('')
    }, []);

    const handleSearch = (term) => {
        setSearchTerm(term);
        fetchAPI(term);
        console.log(`Searching for: ${term}`);
    };

    function CheckboxComponent({ list_of_filter_types }) {
        return (
            <div>
                {list_of_filter_types.map((type) => (
                    <div className="form-check text-secondary" key={type}>
                        <input
                            className="form-check-input checkbox-type"
                            type="checkbox"
                            id={type}
                            defaultChecked={true}
                        />
                        <label className="form-check-label" htmlFor={type}>
                            {type}
                        </label>
                    </div>
                ))}
            </div>
        );
    }

    function TableComponent({ results }) {
        return(
            <div>
                <table className="table table-hover" >
                    <thead>
                    <tr>
                        <th scope="col" className="text-secondary">Type</th>
                        <th scope="col" className="text-secondary">ID</th>
                        <th scope="col" className="text-secondary w-50">Name</th>
                        <th scope="col" className="text-secondary">Domains</th>
                    </tr>
                    </thead>

                    <tbody className="table-group-divider ">
                    {results.map((result) => (
                        <tr>
                            <td>{result[0]}</td>
                            <td>{result[1]}</td>
                            <td>{result[2]}</td>
                            <td>{result[3]}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>

            </div>
        )
    }


    return (
        <div className="container-fluid mt-lg-5">
            <div className="d-flex px-4" >

                {/* FILTERS */}
                <div className="col text-start">
                    <p className="h4 text-secondary fw-bold"  style={{marginTop:'50px'}}> Filters </p>
                    <div className="ms-3 me-3 mt-4">
                        <p className="h6 text-secondary">Object type:</p>
                        <CheckboxComponent list_of_filter_types={list_of_filter_types}/>

                        <p className="h6 mt-3 text-secondary">Domain of search:</p>
                        <CheckboxComponent list_of_filter_types={list_of_filter_domains}/>

                    </div>
                </div>

                <div className="d-flex col-1 justify-content-center align-items-center p-0"
                     style={{height: 'auto', width: '15px'}}>
                    <div className="vr thick-vr border-primary"></div>
                </div>

                {/* SEARCH AND RESULTS */}
                <div className="container-fluid" style={{marginTop:'50px'}}>
                    <SearchBar onSearch={handleSearch} finderRef={finderRef}/>
                    <TableComponent results={currentRecords}/>
                    <Pagination
                        nPages={nPages}
                        currentPage={currentPage}
                        setCurrentPage={setCurrentPage}
                    />
                </div>

            </div>
        </div>

    );
};

export default ManualSearch;