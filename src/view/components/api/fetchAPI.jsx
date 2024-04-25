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

export const fetchDataCampaignAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data/get_campaign`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}

export const fetchDataToolAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data/get_tool_malware`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}

export const fetchDataMalwareAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data/get_tool_malware`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}

export const fetchDataMitigationAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data/get_mitigation`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}

export const fetchDataAssetAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data/get_asset`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}

export const fetchDataVulnerabilityAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data/get_vulnerability`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}
