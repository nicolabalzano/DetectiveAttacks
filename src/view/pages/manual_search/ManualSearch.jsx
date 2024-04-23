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
    const [arrowDirectionTabelOrder, setArrowDirectionTableOrder] = useState();

    const [loading, setLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(1);
    const [recordsPerPage, setRecordsPerPage] = useState(18);

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
        //set direction of arrows in table to default
        if (response.data.results.length > 0) {
            setArrowDirectionTableOrder(new Array(response.data.results[0].length).fill('down'));
        } else {
            setArrowDirectionTableOrder([]);
        }
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
        let newArrowDirectionTableOrder = [...arrowDirectionTabelOrder];
        if (arrowDirectionTabelOrder[index] === 'down') {
            newArrowDirectionTableOrder[index] = 'up';
            setArrowDirectionTableOrder(newArrowDirectionTableOrder);
            setResults([...results].sort((a, b) => a[index] > b[index] ? 1 : -1));
        }
        else {
            newArrowDirectionTableOrder[index] = 'down';
            setArrowDirectionTableOrder(newArrowDirectionTableOrder);
            setResults([...results].sort((a, b) => a[index] < b[index] ? 1 : -1));
        }
        console.log('Sorting by index: ', index);
    }

    function TableComponent({results}) {
        return(
            <div className="search-result">
                <table className="table table-hover table-sorting" >
                    <thead>
                    <tr>
                        <th scope="col" role="button" className="text-secondary" onClick={()=>handleSort(0)}>Type<i className={`bi bi-arrow-${arrowDirectionTabelOrder[0]}`}></i></th>
                        <th scope="col" role="button" className="text-secondary" onClick={()=>handleSort(1)}>ID<i className={`bi bi-arrow-${arrowDirectionTabelOrder[1]}`}></i></th>
                        <th scope="col" role="button" className="text-secondary w-50" onClick={()=>handleSort(2)}>Name<i className={`bi bi-arrow-${arrowDirectionTabelOrder[2]}`}></i></th>
                        <th scope="col" role="button" className="text-secondary" onClick={()=>handleSort(3)}>Domains<i className={`bi bi-arrow-${arrowDirectionTabelOrder[3]}`}></i></th>
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


                        <div className="mt-5">
                            <span className="fs-6">N° of rows</span>
                            <input type="number" className="w-auto mt-3 border border-1 border-secondary rounded num-rows-selector" min="1" max="300"
                                   defaultValue={recordsPerPage}
                            onChange={(e)=>setRecordsPerPage(e.target.value)}/>
                        </div>
                    </div>
                </div>

                <div className="d-flex col-1 justify-content-center align-items-center p-0"
                     style={{height: 'auto', width: '15px'}}>
                    <div className="vr thick-vr border-primary"></div>
                </div>

                {/* SEARCH AND RESULTS */}
                {
                    loading ? (
                        <div className="text-center text-secondary mt-5 search-result">
                            <div className="spinner-border text-primary" role="status">
                                <span className="visually-hidden">Loading...</span>
                            </div>
                        </div>
                    ) : (

                        <div className="container-fluid" style={{marginTop: '50px'}}>
                            <SearchBar onSearch={handleSearch} finderRef={finderRef}/>
                            {results.length === 0 ? (
                            <div className="text-center text-secondary mt-5 search-result">
                                <h3>No results found</h3>
                            </div>
                            ) : (
                            <div className="">
                                <TableComponent results={currentRecords}/>
                                <div className="d-flex justify-content-center text-primary mt-4">
                                    <Stack spacing={2}>
                                        {/* PAGINATION */}
                                        <Pagination count={nPages} page={currentPage}
                                                    onChange={(event, page) => setCurrentPage(page)}
                                                    className="custom-pagination"/>
                                    </Stack>
                                </div>
                            </div>
                            )}
                        </div>
                    )
                }
            </div>
        </div>

    );
};

export default ManualSearch;