import React, {useEffect, useRef, useState} from 'react';
import SearchBar from "../../components/search_bar/SearchBar.jsx";
import './manual_search.scss';
import {Box, Pagination, Skeleton, Stack} from "@mui/material";
import {fetchDataAPI, fetchFilterAPI} from "../../components/api/fetchAPI.jsx";
import {navigateToThreats} from "./HandleRoutingThreats.jsx";

const ManualSearch = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [listOfFilterTypes, setListOfFilterTypes] = useState(['all']);
    const [selectedTypes, setSelectedTypes] = useState(['all']);
    const [listOfFilterDomains, setListOfFilterDomains] = useState(['all']);
    const [selectedDomains, setSelectedDomains] = useState(['all']);
    const [results, setResults] = useState([]);
    const [arrowDirectionTabelOrder, setArrowDirectionTableOrder] = useState();

    const [loading, setLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(1);
    const [recordsPerPage, setRecordsPerPage] = useState(18);

    const indexOfLastRecord = currentPage * recordsPerPage;
    const indexOfFirstRecord = indexOfLastRecord - recordsPerPage;
    const currentRecords = results.slice(indexOfFirstRecord, indexOfLastRecord);
    const nPages = Math.ceil(results.length / recordsPerPage)

    // FETCH DATA FROM API and SET FILTERS on startup
    useEffect(() => {
        // FETCH FILTERS FROM API
        fetchFilterAPI().then(r=>{
            setListOfFilterTypes(r.data.list_of_filter_types);
            setListOfFilterDomains(r.data.list_of_filter_domains);
            setSelectedDomains(r.data.list_of_filter_domains);
            setSelectedTypes(r.data.list_of_filter_types);
        });

        const root_element = document.getElementById('root');
        root_element.classList.remove('d-flex')
        root_element.classList.remove('align-content-center')
        root_element.classList.remove('justify-content-center')
        root_element.classList.remove('align-items-center')
        root_element.style.margin = "0";
        root_element.style.height = "100vh";
    }, []);

    useEffect(() => {
        setLoading(true);
        // FETCH DATA FROM API
        fetchDataAPI(searchTerm, selectedTypes, selectedDomains).then(r =>{
            setResults(r.data.results);
            //set direction of arrows in table to default
            if (r.data.results.length > 0) {
                setArrowDirectionTableOrder(new Array(r.data.results[0].length).fill('down'));
            } else {
                setArrowDirectionTableOrder([]);
            }
            setLoading(false);
        });
    }, [searchTerm, selectedTypes, selectedDomains]);

    const handleSearch = (term) => {
        setSearchTerm(term);
        setCurrentPage(1);
    };

    const handleCheckboxChange = (event, setSelected, selected) => {
        const { checked, id } = event.target;
        if (checked) {
            setSelected((prevSelected) => [...prevSelected, id]);
        } else {
            setSelected((prevSelected) => prevSelected.filter((type) => type !== id));
        }
        setCurrentPage(1);
    };

    function CheckboxComponent({ list_of_filter, setSelected, selected}) {
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

    }

    function TableComponent({results}) {
        return(
            <div className="search-result">
                <table className="table table-hover table-sorting" >
                    <thead>
                    <tr >
                        <th scope="col" role="button" className="text-secondary" onClick={()=>handleSort(0)}>Type<i className={`bi bi-arrow-${arrowDirectionTabelOrder[0]}`}></i></th>
                        <th scope="col" role="button" className="text-secondary" onClick={()=>handleSort(1)}>ID<i className={`bi bi-arrow-${arrowDirectionTabelOrder[1]}`}></i></th>
                        <th scope="col" role="button" className="text-secondary w-50" onClick={()=>handleSort(2)}>Name<i className={`bi bi-arrow-${arrowDirectionTabelOrder[2]}`}></i></th>
                        <th scope="col" role="button" className="text-secondary" onClick={()=>handleSort(3)}>Domains<i className={`bi bi-arrow-${arrowDirectionTabelOrder[3]}`}></i></th>
                    </tr>
                    </thead>

                    <tbody className="table-group-divider ">
                    {results.map((result, index) => (
                        <tr key={index} className="border-b border-secondary" role="button" onClick={()=>navigateToThreats(result[1], result[0])}>
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
        <div className="container-fluid">
            <div className="d-flex px-4" >

                {/* FILTERS */}
                <div className="col text-start" style={{marginTop:'70px'}}>
                    <p className="h4 text-secondary fw-bold"> Filters </p>
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


                        <div className="mt-3">
                            <span className="fs-6 fw-semibold text-secondary">N° of rows</span>
                            <input type="number" className="w-auto rounded num-rows-selector" min="1" max="300"
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
                <div className="container-fluid" style={{marginTop: '70px'}}>
                    <SearchBar onSearch={handleSearch} />
                    {
                        loading ? (
                            <div className="text-center text-secondary mt-5 search-result">
                                <Box sx={{ width: 1 }}>
                                    {[...Array(recordsPerPage)].map((_, index) => (
                                        <Skeleton key={index} animation="wave" height="50px" />
                                    ))}
                                </Box>
                            </div>
                        ) : (
                            results.length === 0 ? (
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
                            )
                        )
                    }
                </div>

            </div>
        </div>

    );
};

export default ManualSearch;