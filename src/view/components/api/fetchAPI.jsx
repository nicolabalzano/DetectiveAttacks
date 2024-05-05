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

// FETCH PLATFORMS DATA
export const fetchDataPlatforms = async () => {
    return await axios.get(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data/get_platforms`);
}

// FETCH DOMAINS DATA
export const fetchDataDomains = async () => {
    return await axios.get(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data/get_domains`);
}

// FETCH ATTACK PATTERNS DATA
export const fetchDataAttackAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data/get_attack_pattern`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}

// FETCH ATTACK PATTERNS GROUPED BY CKC PHASES
export const fetchDataAttackPatternsGroupedByPhaseAPI = async () => {
    let url = new URL(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data/get_attack_patterns_grouped_by_CKCP`);
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

export const fetchDataAssetAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data/get_asset`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}


export const fetchDataIntrusionSetAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data/get_intrusion_set`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}


export const fetchDataVulnerabilityAPI = async (id) => {
    let params = {id: id};
    let url = new URL(`${import.meta.env.VITE_IP_PORT_TO_FLASK}/api/get_data/get_vulnerability`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    return await axios.get(url.toString());
}
