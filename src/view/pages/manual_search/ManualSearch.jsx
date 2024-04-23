import React, {useEffect, useRef, useState} from 'react';
import SearchBar from "../../components/search_bar/SearchBar.jsx";
import axios from "axios";
// import Pagination from "../../components/pagination/Pagination.jsx";
import './manual_search.scss';
import {Pagination, Stack} from "@mui/material";

const ManualSearch = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [listOfFilterTypes, setListOfFilterTypes] = useState(['all']);
    const [selectedTypes, setSelectedTypes] = useState([]);
    const [listOfFilterDomains, setListOfFilterDomains] = useState(['all']);
    const [selectedDomains, setSelectedDomains] = useState([]);
    const [results, setResults] = useState([]);

    const [loading, setLoading] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [recordsPerPage] = useState(18);

    const indexOfLastRecord = currentPage * recordsPerPage;
    const indexOfFirstRecord = indexOfLastRecord - recordsPerPage;
    const currentRecords = results.slice(indexOfFirstRecord, indexOfLastRecord);
    const nPages = Math.ceil(results.length / recordsPerPage)

    const finderRef = useRef(null);

    const fetchAPI = async () => {
        setLoading(true);
        // REQUEST TO FLASK API
        let params = {search: searchTerm, types: selectedTypes, domains: selectedDomains};
        let url = new URL(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data`);
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
        const response = await axios.get(url.toString());
        setResults(response.data.results);
        setLoading(false);
        console.log(response.data);
        return response;
    };

    // FETCH DATA FROM API and SET FILTERS on startup
    useEffect(() => {
        const fetchFilters = async () => {
            const response = await fetchAPI();

            setListOfFilterTypes(response.data.list_of_filter_types);
            setListOfFilterDomains(response.data.list_of_filter_domains);
            setSelectedDomains(response.data.list_of_filter_domains);
            setSelectedTypes(response.data.list_of_filter_types);
        };

        fetchFilters();
    }, []);

    useEffect(() => {
        fetchAPI();
    }, [searchTerm, selectedTypes, selectedDomains]);

    const handleSearch = (term) => {
        setSearchTerm(term);
    };

    const handleCheckboxChange = (event, setSelected, selected) => {
        const { checked, id } = event.target;
        if (checked) {
            setSelected((prevSelected) => [...prevSelected, id]);
        } else {
            setSelected((prevSelected) => prevSelected.filter((type) => type !== id));
        }
    };

    function CheckboxComponent({ list_of_filter, setSelected, selected}) {
        useEffect(() => {
        }, [selected]);

        return (
            <div>
                {list_of_filter.map((type) => (
                    <div className="form-check text-secondary" key={type}>
                        <input
                            className="form-check-input checkbox-type"
                            type="checkbox"
                            id={type}
                            onChange={(event => handleCheckboxChange(event, setSelected, selected))}
                            checked={selected.includes(type)}
                        />
                        <label className="form-check-label" htmlFor={type}>
                            {type}
                        </label>
                    </div>
                ))}
            </div>
        );
    }

    function handleSort(index) {
        const table = document.querySelector('.table-sorting');
        const th = table.querySelectorAll('th')[index];
        if (th.innerHTML.includes('bi-arrow-up')) {
            th.innerHTML = th.innerHTML.replace('<i class="bi bi-arrow-up"></i>', '<i class="bi bi-arrow-down"></i>');
            setResults([...results].sort((a, b) => a[index] > b[index] ? 1 : -1));
        }
        else {
            th.innerHTML = th.innerHTML.replace('<i class="bi bi-arrow-down"></i>', '<i class="bi bi-arrow-up"></i>');
            setResults([...results].sort((a, b) => a[index] < b[index] ? 1 : -1));
        }
        console.log('Sorting by index: ', index);
    }

    function TableComponent({results}) {
        if (results.length === 0) {
            return (
                <div className="text-center text-secondary mt-5">
                    <h3>No results found</h3>
                </div>
            );
        }
        return(
            <div>
                <table className="table table-hover table-sorting" >
                    <thead>
                    <tr>
                        <th scope="col" role="button" className="text-secondary" onClick={()=>handleSort(0)}>Type<i className="bi bi-arrow-down"></i></th>
                        <th scope="col" role="button" className="text-secondary" onClick={()=>handleSort(1)}>ID<i className="bi bi-arrow-down"></i></th>
                        <th scope="col" role="button" className="text-secondary w-50" onClick={()=>handleSort(2)}>Name<i className="bi bi-arrow-down"></i></th>
                        <th scope="col" role="button" className="text-secondary" onClick={()=>handleSort(3)}>Domains<i className="bi bi-arrow-down"></i></th>
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
                        <CheckboxComponent
                            list_of_filter={listOfFilterTypes}
                            setSelected={setSelectedTypes}
                            selected={selectedTypes}
                        />

                        <p className="h6 mt-3 text-secondary">Domain of search:</p>
                        <CheckboxComponent
                            list_of_filter={listOfFilterDomains}
                            setSelected={setSelectedDomains}
                            selected={selectedDomains}
                        />
                    </div>
                </div>

                <div className="d-flex col-1 justify-content-center align-items-center p-0"
                     style={{height: 'auto', width: '15px'}}>
                    <div className="vr thick-vr border-primary"></div>
                </div>

                {/* SEARCH AND RESULTS */}
                <div className="container-fluid" style={{marginTop: '50px'}}>
                    <SearchBar onSearch={handleSearch} finderRef={finderRef}/>

                    <div className="search-result">
                        <TableComponent results={currentRecords}/>
                        <div className="d-flex justify-content-center text-primary mt-4">
                            <Stack spacing={2}>
                                <Pagination count={nPages} page={currentPage}
                                            onChange={(event, page) => setCurrentPage(page)}
                                            className="custom-pagination"/>
                            </Stack>
                        </div>
                    </div>
                </div>


            </div>
        </div>

    );
};

export default ManualSearch;