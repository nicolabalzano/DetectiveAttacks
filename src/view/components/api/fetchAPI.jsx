import axios from "axios";

// FETCH ALL THREATS
export const fetchDataAPI = async (searchTerm, selectedTypes, selectedDomains) => {
    // REQUEST TO FLASK API
    let params = {search: searchTerm, types: selectedTypes, domains: selectedDomains};
    let url = new URL(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
};

// FETCH FILTERS FOR RESEARCH
export const fetchFilterAPI = async () => {
    return await axios.get(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_filters`);
}

// FETCH ATTACK DATA
export const fetchDataAttackAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data/get_attack`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}

